#!/usr/bin/env python3
"""
Automated satellite fetch for the ecosystem-digital-twin skill.

Searches a public STAC catalogue for satellite scenes over an area of
interest, records the scenes and their asset links, downloads the red /
near-infrared bands on request, and computes a simple NDVI indicator
where the bands are available. Every product is registered as a virtual
sensor (references/data-sources.md: a satellite proxy becomes a
registered virtual sensor in the Object Passport).

A satellite is a PERIODIC virtual sensor, never real-time: Sentinel-2
revisits in ~5 days, Sentinel-1 in 6-12 days, Landsat in 16 days, plus
hours of processing before a scene is usable. Real-time warning uses
ground telemetry (gauges, sondes, meteo stations); the satellite gives
the context and the trend between passes. The manifest records the
retrieval date and the scene dates, so no one mistakes a scene date for
"now" (rule §19: source and date on every indicator).

Catalogues:
- Planetary Computer STAC (https://planetarycomputer.microsoft.com/api/stac/v1)
  -- search needs no key; collections sentinel-2-l2a, landsat-c2-l2,
  sentinel-1-rtc (verified live 2026-10-28).
- Copernicus Data Space STAC (https://catalogue.dataspace.copernicus.eu/stac/v1)
  -- search is open; DOWNLOAD needs a free account and a token
  (--cdse-token). The catalogue was unreachable from this environment on
  2026-10-28: verify access at build time; services change.

Standard library only for search, download, and NDVI arithmetic.
Reading GeoTIFF bands needs the optional `rasterio` package: without it
the script records the scenes and asset links and marks the computation
as deferred -- it never invents numbers.

Usage:
  python3 scripts/fetch_satellite.py --source sentinel-2 \
      --bbox 85.5,28.2,86.0,28.5 --start 2026-08-01 --end 2026-08-31 --check
  python3 scripts/fetch_satellite.py --source landsat \
      --bbox 85.5,28.2,86.0,28.5 --start 2026-08-01 --end 2026-08-31 \
      --download --compute-ndvi --out ./satellite-fetch
  python3 scripts/fetch_satellite.py --source sentinel-1 \
      --bbox 85.5,28.2,86.0,28.5 --start 2026-08-01 --end 2026-08-31 --check

Exit codes: 0 ok; 2 usage error; 3 catalogue / network / auth failure.
A 429 response stops the run: never hammer a rate-limited catalogue.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone

UA = "ecosystem-digital-twin/2.8 satellite-fetch"
TIMEOUT = 25

CATALOGS = {
    "planetary-computer": "https://planetarycomputer.microsoft.com/api/stac/v1",
    "copernicus": "https://catalogue.dataspace.copernicus.eu/stac/v1",
}

# Band keys are the asset keys in the Planetary Computer STAC items,
# verified live 2026-10-28. Other catalogues may key assets differently:
# parse_scenes falls back to every data-role asset when the expected keys
# are absent, and records what it found instead of guessing.
SOURCES = {
    "sentinel-2": {
        "pc_collection": "sentinel-2-l2a",
        "cdse_collection": "SENTINEL-2",
        "red": "B04",
        "nir": "B08",
        "ndvi": True,
        "cloud": True,
        "note": "Multispectral 10-20 m, ~5-day revisit.",
    },
    "landsat": {
        "pc_collection": "landsat-c2-l2",
        "cdse_collection": None,
        "red": "red",
        "nir": "nir08",
        "ndvi": True,
        "cloud": True,
        "note": "Multispectral 30 m, 16-day revisit; archive back to 1984.",
    },
    "sentinel-1": {
        "pc_collection": "sentinel-1-rtc",
        "cdse_collection": "SENTINEL-1",
        "red": None,
        "nir": None,
        "ndvi": False,
        "cloud": False,
        "note": "SAR backscatter (VV/VH). Displacement needs InSAR "
                "processing of a pair (SNAP / ASF HyP3), not computed here.",
    },
}


class FetchError(Exception):
    """Catalogue, network, or auth failure: reported, never silent."""


def parse_bbox(text):
    try:
        parts = [float(p) for p in text.split(",")]
    except ValueError:
        raise ValueError(f"bbox must be four numbers 'minlon,minlat,maxlon,maxlat', got: {text!r}")
    if len(parts) != 4:
        raise ValueError(f"bbox must be four numbers 'minlon,minlat,maxlon,maxlat', got: {text!r}")
    minlon, minlat, maxlon, maxlat = parts
    if not (minlon < maxlon and minlat < maxlat):
        raise ValueError(f"bbox corners out of order: {text!r}")
    if not (-180.0 <= minlon <= 180.0 and -180.0 <= maxlon <= 180.0):
        raise ValueError(f"bbox longitudes must be within -180..180: {text!r}")
    if not (-90.0 <= minlat <= 90.0 and -90.0 <= maxlat <= 90.0):
        raise ValueError(f"bbox latitudes must be within -90..90: {text!r}")
    return parts


def parse_day(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD, got: {text!r}")


def stac_search(base, collection, bbox, start, end, limit, timeout):
    """GET {base}/search; returns the parsed STAC FeatureCollection."""
    params = {
        "collections": collection,
        "bbox": ",".join(str(v) for v in bbox),
        "datetime": f"{start.isoformat()}T00:00:00Z/{end.isoformat()}T23:59:59Z",
        "limit": limit,
    }
    url = base.rstrip("/") + "/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            raise FetchError(
                f"catalogue rate-limited (HTTP 429) at {base}: stop, retry later, "
                "do not hammer the catalogue.")
        if exc.code in (401, 403):
            raise FetchError(
                f"catalogue refused access (HTTP {exc.code}) at {base}: the search "
                "may need an account or a token; verify access at build time.")
        raise FetchError(f"catalogue request failed (HTTP {exc.code}) at {base}: "
                         f"{exc.reason}.")
    except urllib.error.URLError as exc:
        raise FetchError(f"catalogue unreachable at {base}: {exc.reason}. "
                         "Check the network and the catalogue URL; verify access "
                         "at build time.")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise FetchError(f"catalogue at {base} returned a non-JSON response.")
    if not isinstance(data, dict) or not isinstance(data.get("features"), list):
        raise FetchError(f"catalogue at {base} returned no STAC features list.")
    return data


def parse_scenes(data, source):
    """One record per STAC feature: id, datetime, cloud cover, band links."""
    spec = SOURCES[source]
    scenes = []
    for feat in data.get("features", []):
        props = feat.get("properties", {}) or {}
        assets = feat.get("assets", {}) or {}
        bands = {}
        for key in (spec["red"], spec["nir"]):
            if key is None:
                continue
            asset = assets.get(key, {}) or {}
            href = asset.get("href")
            roles = asset.get("roles", []) or []
            if href and (not roles or "data" in roles):
                bands[key] = href
        available = sorted(k for k, a in assets.items()
                           if isinstance(a, dict) and a.get("href")
                           and (not a.get("roles") or "data" in a["roles"]))
        cloud = props.get("eo:cloud_cover")
        scenes.append({
            "id": feat.get("id"),
            "datetime": props.get("datetime"),
            "collection": feat.get("collection"),
            "cloud_cover": cloud if isinstance(cloud, (int, float)) else None,
            "bands": bands,
            "assets_available": available,
        })
    return scenes


def filter_cloud(scenes, max_cloud):
    """Drop scenes cloudier than max_cloud. Scenes with no cloud value are
    kept -- an unmeasured cloud cover is a gap, not a reason to drop."""
    kept, dropped = [], 0
    for scene in scenes:
        cloud = scene["cloud_cover"]
        if cloud is not None and cloud > max_cloud:
            dropped += 1
            continue
        kept.append(scene)
    return kept, dropped


def ndvi_from_arrays(red, nir):
    """NDVI = (NIR - red) / (NIR + red), pure Python. A zero denominator
    (both bands zero) is not a measurement: None, never an invented 0."""
    out = []
    for r, n in zip(red, nir):
        denom = n + r
        out.append(None if denom == 0 else (n - r) / denom)
    return out


def ndvi_stats(values):
    """Mean / min / max over valid pixels only; count valid and total."""
    valid = [v for v in values if v is not None]
    if not valid:
        return {"mean": None, "min": None, "max": None,
                "n_valid": 0, "n_total": len(values)}
    return {"mean": round(sum(valid) / len(valid), 4),
            "min": round(min(valid), 4), "max": round(max(valid), 4),
            "n_valid": len(valid), "n_total": len(values)}


def compute_ndvi_from_files(red_path, nir_path):
    """NDVI stats from two GeoTIFF band files, downsampled to at most
    512x512 pixels. Returns (status, payload): 'computed' with stats, or
    'deferred' when the optional rasterio package is absent."""
    try:
        import rasterio
        from rasterio.enums import Resampling
    except ImportError:
        return ("deferred", {
            "status": "deferred",
            "reason": "rasterio (optional GIS tooling) is required to read "
                      "GeoTIFF bands; scenes and asset links are recorded, "
                      "computation deferred -- no numbers invented."})
    with rasterio.open(red_path) as red_src, rasterio.open(nir_path) as nir_src:
        red = red_src.read(1, out_shape=(512, 512),
                           resampling=Resampling.average)
        nir = nir_src.read(1, out_shape=(512, 512),
                           resampling=Resampling.average)
    values = ndvi_from_arrays(red.flatten().tolist(), nir.flatten().tolist())
    stats = ndvi_stats(values)
    stats.update({"status": "computed",
                  "downsampled_to": "512x512",
                  "note": "Statistics are computed on the downsampled "
                          "preview, not full resolution; record this with "
                          "the value."})
    return ("computed", stats)


def download(url, dest, timeout):
    """Download one asset; auth failures name the remedy, never silence."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp, \
                open(dest, "wb") as fh:
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                fh.write(chunk)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise FetchError(
                f"download refused (HTTP {exc.code}) for {url}: the asset "
                "needs signing or an account -- for Planetary Computer sign "
                "the URL through the data API; for Copernicus pass "
                "--cdse-token.")
        raise FetchError(f"download failed (HTTP {exc.code}) for {url}: "
                         f"{exc.reason}.")
    except urllib.error.URLError as exc:
        raise FetchError(f"download failed for {url}: {exc.reason}.")
    return dest


def register_virtual_sensor(source, collection, bbox, start, end, ndvi_status):
    """The registration record for the Object Passport (§1 virtual sensor)."""
    spec = SOURCES[source]
    if spec["ndvi"]:
        name = f"satellite-{source}-ndvi"
        quantity, formula = "NDVI", "(NIR - red) / (NIR + red)"
    else:
        name = f"satellite-{source}-scenes"
        quantity, formula = "scene record", None
    return {
        "name": name,
        "quantity": quantity,
        "formula": formula,
        "source": source,
        "collection": collection,
        "bbox": bbox,
        "date_range": [start.isoformat(), end.isoformat()],
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "validity_window": "until the next pass (see the latency table in "
                           "references/data-sources.md); a satellite is a "
                           "periodic virtual sensor, never real-time.",
        "status": ndvi_status,
    }


def build_parser():
    p = argparse.ArgumentParser(
        prog="fetch_satellite.py",
        description="Fetch satellite scenes from a public STAC catalogue and "
                    "register the product as a virtual sensor. A satellite "
                    "is a periodic snapshot (Sentinel-2 ~5 days, Sentinel-1 "
                    "6-12 days, Landsat 16 days), never real-time.")
    p.add_argument("--source", required=True,
                   choices=sorted(SOURCES),
                   help="satellite source: sentinel-2, landsat, sentinel-1")
    p.add_argument("--bbox", required=True,
                   help="area of interest 'minlon,minlat,maxlon,maxlat'")
    p.add_argument("--start", required=True, help="first date YYYY-MM-DD")
    p.add_argument("--end", required=True, help="last date YYYY-MM-DD")
    p.add_argument("--limit", type=int, default=5,
                   help="max scenes to list (default 5)")
    p.add_argument("--max-cloud", type=float, default=20.0,
                   help="drop optical scenes cloudier than this percent "
                        "(default 20; scenes with no cloud value are kept)")
    p.add_argument("--catalog", default="planetary-computer",
                   choices=sorted(CATALOGS),
                   help="STAC catalogue (default planetary-computer, no key)")
    p.add_argument("--catalog-url", default=None,
                   help="override the catalogue base URL (tests, mirrors)")
    p.add_argument("--cdse-token", default=None,
                   help="Copernicus Data Space access token, for downloads")
    p.add_argument("--check", action="store_true",
                   help="search only: list scenes, write the manifest, "
                        "download nothing")
    p.add_argument("--download", action="store_true",
                   help="download the red / NIR bands of the least-cloudy "
                        "scene (all kept scenes with --all)")
    p.add_argument("--all", action="store_true",
                   help="with --download: download bands for every kept scene")
    p.add_argument("--compute-ndvi", action="store_true",
                   help="compute NDVI stats from the downloaded bands "
                        "(needs --download and the optional rasterio package)")
    p.add_argument("--out", default="./satellite-fetch",
                   help="output directory for manifest.json (default "
                        "./satellite-fetch)")
    p.add_argument("--stac-file", default=None,
                   help="offline: read a recorded STAC response from this "
                        "file instead of the network")
    p.add_argument("--timeout", type=int, default=TIMEOUT,
                   help=f"network timeout in seconds (default {TIMEOUT})")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        bbox = parse_bbox(args.bbox)
        start = parse_day(args.start)
        end = parse_day(args.end)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if start > end:
        print("error: --start must not be after --end", file=sys.stderr)
        return 2
    if args.limit < 1:
        print("error: --limit must be at least 1", file=sys.stderr)
        return 2
    if args.check and args.download:
        print("error: --check and --download conflict", file=sys.stderr)
        return 2
    if args.compute_ndvi and not args.download:
        print("error: --compute-ndvi needs --download", file=sys.stderr)
        return 2
    spec = SOURCES[args.source]
    base = args.catalog_url or CATALOGS[args.catalog]
    collection = (spec["cdse_collection"] if args.catalog == "copernicus"
                  else spec["pc_collection"])
    if args.catalog == "copernicus" and collection is None:
        print(f"error: {args.source} is not served by the Copernicus Data "
              "Space; use --catalog planetary-computer.", file=sys.stderr)
        return 2
    if args.catalog == "copernicus" and args.download and not args.cdse_token:
        print("error: Copernicus download needs a free account token "
              "(--cdse-token); search is open, download is not.",
              file=sys.stderr)
        return 2

    notes = ["A satellite is a periodic virtual sensor, never real-time: "
             "Sentinel-2 ~5 days, Sentinel-1 6-12 days, Landsat 16 days, "
             "plus processing latency. Real-time warning uses ground "
             "telemetry; the satellite gives context and trend between passes."]
    if args.stac_file:
        try:
            with open(args.stac_file, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"error: cannot read --stac-file {args.stac_file}: {exc}",
                  file=sys.stderr)
            return 2
        notes.append(f"Offline mode: scenes read from recorded STAC response "
                     f"{args.stac_file}, no network used.")
    else:
        try:
            data = stac_search(base, collection, bbox, start, end,
                               args.limit, args.timeout)
        except FetchError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 3

    scenes = parse_scenes(data, args.source)
    if spec["cloud"]:
        scenes, dropped = filter_cloud(scenes, args.max_cloud)
        if dropped:
            notes.append(f"{dropped} scene(s) dropped as cloudier than "
                         f"{args.max_cloud}% (cloud cover as reported by the "
                         "catalogue).")

    downloads = []
    ndvi = {"status": "not-computed"}
    exit_code = 0
    if args.download:
        targets = scenes if args.all else scenes[:1]
        if not targets:
            notes.append("Nothing to download: no scenes kept.")
        for scene in targets:
            for band_key in (spec["red"], spec["nir"]):
                if band_key is None:
                    continue
                href = scene["bands"].get(band_key)
                if not href:
                    downloads.append({"scene": scene["id"], "band": band_key,
                                      "status": "missing",
                                      "reason": "band asset not in the "
                                                "catalogue response"})
                    continue
                dest = os.path.join(args.out, f"{scene['id']}_{band_key}.tif")
                try:
                    os.makedirs(args.out, exist_ok=True)
                    download(href, dest, args.timeout)
                    downloads.append({"scene": scene["id"], "band": band_key,
                                      "file": dest, "status": "downloaded"})
                except FetchError as exc:
                    downloads.append({"scene": scene["id"], "band": band_key,
                                      "status": "failed", "reason": str(exc)})
                    print(f"error: {exc}", file=sys.stderr)
                    exit_code = 3
        if args.compute_ndvi and exit_code == 0:
            done = {d["band"]: d["file"] for d in downloads
                    if d["status"] == "downloaded"}
            if spec["red"] in done and spec["nir"] in done:
                status, payload = compute_ndvi_from_files(
                    done[spec["red"]], done[spec["nir"]])
                ndvi = payload
                if status == "deferred":
                    print(f"warning: {payload['reason']}", file=sys.stderr)
            else:
                ndvi = {"status": "not-computed",
                        "reason": "red / NIR bands not downloaded; NDVI "
                                  "needs both bands."}
    elif spec["ndvi"]:
        ndvi = {"status": "not-computed",
                "reason": "run with --download --compute-ndvi to compute "
                          "NDVI from the bands (needs the optional rasterio "
                          "package)."}
    else:
        ndvi = {"status": "not-applicable",
                "reason": spec["note"]}

    sensor = register_virtual_sensor(
        args.source, collection, bbox, start, end,
        ndvi.get("status", "not-computed"))
    manifest = {
        "tool": "fetch_satellite.py",
        "version": "2.8",
        "source": args.source,
        "catalog": args.catalog,
        "catalog_url": base,
        "collection": collection,
        "bbox": bbox,
        "date_range": [start.isoformat(), end.isoformat()],
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "max_cloud": args.max_cloud if spec["cloud"] else None,
        "scenes": scenes,
        "downloads": downloads,
        "ndvi": ndvi,
        "virtual_sensor": sensor,
        "notes": notes,
    }
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "manifest.json"), "w",
              encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    with open(os.path.join(args.out, "virtual-sensor.json"), "w",
              encoding="utf-8") as fh:
        json.dump(sensor, fh, ensure_ascii=False, indent=2)
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
