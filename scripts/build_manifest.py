#!/usr/bin/env python3
"""
Provenance package builder (Phase 6, ecosystem-digital-twin skill).

Reads a small build index (JSON) and writes ro-crate-metadata.json that
conforms to RO-Crate 1.1: metadata descriptor, root dataset (name,
description, datePublished, license), one data entity per dataset, one
SoftwareApplication per model component, one CreateAction per workflow step
(object = inputs, instrument = model, result = outputs), and one
PropertyValue per headline number. Every headline number is therefore
traceable, by machine, to the step, model, and datasets that produced it.

Build index shape (all ids unique across the file):

{
  "name": "Lake X twin - 2027 season package", "description": "...",
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "datePublished": "2027-10-01",                      (optional; default today)
  "datasets": [{"id": "ds-01", "name": "...", "url": "https://..." or "path": "data/x.csv",
                "version": "...", "retrieved": "YYYY-MM-DD", "license": "...",
                "doi": "10.xxxx/...", "kind": "file" | "dataset"}],
  "models":   [{"id": "m-01", "name": "...", "version": "...", "url": "..."}],
  "steps":    [{"id": "st-01", "name": "...", "instrument": "m-01",
                "inputs": ["ds-01"], "parameters": "...", "date": "YYYY-MM-DD"}],
  "outputs":  [{"id": "out-01", "name": "...", "value": 4.2, "unit": "mg/m3",
                "produced_by": "st-01", "headline": true}],
  "mappings": [{"id": "map-01", "dataset": "ds-01",
                "path": "examples/gallery/pond/mappings.csv",
                "standard": "Darwin Core"}],   (optional; one per dataset mapping file)
  "doi": "10.5281/zenodo.23657185",               (optional; package DOI, bare or full URL)
}

Checks (errors stop the build, exit 3): missing required fields; unknown or
duplicate ids; a step without a known model; a step input that is neither a
dataset nor an earlier output; an output without its producing step; a web
dataset without its retrieval date; a model without a version.
--report FILE also requires every headline output to be cited in the report
as [out-id] and every cited [id] to exist in the index.
--registry FILE ties forecasts to the package: the forecast registry's hash
chain must verify, and every input id of every registered forecast must be a
dataset or output of this build index.

Signposting (FAIR, signposting.org): the Root Dataset of the crate carries
explicit typed links — cite-as (the package DOI, from "doi", never invented:
absent when no DOI is given), describedby (ro-crate-metadata.json itself),
license (the index license, included only when given as an http(s) URL).
The same relations belong in HTTP Link headers when the package is served
over HTTP; the crate entries are the static, file-based form of the same
links.

Usage:
  python3 build_manifest.py build.json --out-dir package/
  python3 build_manifest.py build.json --check --report report.md --registry reg.jsonl
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import date

CONTEXT = "https://w3id.org/ro/crate/1.1/context"
CONFORMS = "https://w3id.org/ro/crate/1.1"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CITE_RE = re.compile(r"\[((?:out|ds|m|st)-[A-Za-z0-9_.-]+)\]")


def validate(idx, base_dir):
    errors, warnings = [], []
    for key in ("name", "description", "license"):
        if not str(idx.get(key, "")).strip():
            errors.append(f"root: '{key}' is required")
    if idx.get("datePublished") and not DATE_RE.match(str(idx["datePublished"])):
        errors.append("root: datePublished must be YYYY-MM-DD")
    seen = {}

    def register(kind, item):
        i = item.get("id")
        if not i:
            errors.append(f"{kind}: an entry has no 'id'")
            return None
        if i in seen:
            errors.append(f"duplicate id '{i}' ({seen[i]} and {kind})")
        seen[i] = kind
        return i

    datasets = {}
    for d in idx.get("datasets", []):
        i = register("dataset", d)
        if i is None:
            continue
        datasets[i] = d
        if not d.get("name"):
            errors.append(f"{i}: 'name' is required")
        if not d.get("url") and not d.get("path"):
            errors.append(f"{i}: give 'url' (web data) or 'path' (file in the package)")
        if d.get("url") and not d.get("retrieved"):
            errors.append(f"{i}: web dataset needs 'retrieved' (YYYY-MM-DD)")
        if d.get("retrieved") and not DATE_RE.match(str(d["retrieved"])):
            errors.append(f"{i}: 'retrieved' must be YYYY-MM-DD")
        if not d.get("version") and not d.get("version_note"):
            warnings.append(f"{i}: no 'version' (or 'version_note' saying why none exists)")
        if not d.get("license"):
            warnings.append(f"{i}: no 'license' recorded")
        if d.get("path") and not os.path.exists(os.path.join(base_dir, d["path"])):
            warnings.append(f"{i}: file '{d['path']}' not found next to the package")
    models = {}
    for m in idx.get("models", []):
        i = register("model", m)
        if i is None:
            continue
        models[i] = m
        if not m.get("name"):
            errors.append(f"{i}: 'name' is required")
        if not m.get("version"):
            errors.append(f"{i}: 'version' is required (a result must name the model version)")
    steps = {}
    produced = set()
    outputs_by_step = {}
    for o in idx.get("outputs", []):
        outputs_by_step.setdefault(o.get("produced_by"), []).append(o.get("id"))
    for s in idx.get("steps", []):
        i = register("step", s)
        if i is None:
            continue
        steps[i] = s
        if s.get("instrument") not in models:
            errors.append(f"{i}: instrument '{s.get('instrument')}' is not a known model id")
        if not s.get("inputs"):
            errors.append(f"{i}: 'inputs' must list at least one dataset or earlier output")
        for inp in s.get("inputs", []):
            if inp not in datasets and inp not in produced:
                errors.append(f"{i}: input '{inp}' is neither a dataset nor an output of an earlier step")
        produced.update(outputs_by_step.get(i, []))
    outputs = {}
    for o in idx.get("outputs", []):
        i = register("output", o)
        if i is None:
            continue
        outputs[i] = o
        if not o.get("name"):
            errors.append(f"{i}: 'name' is required")
        if "value" not in o:
            errors.append(f"{i}: 'value' is required")
        if o.get("produced_by") not in steps:
            errors.append(f"{i}: produced_by '{o.get('produced_by')}' is not a known step id")
    mappings = {}
    for mp in idx.get("mappings", []):
        i = register("mapping", mp)
        if i is None:
            continue
        mappings[i] = mp
        if mp.get("dataset") not in datasets:
            errors.append(f"{i}: dataset '{mp.get('dataset')}' is not a known dataset id")
        if not mp.get("path"):
            errors.append(f"{i}: 'path' (the mappings.csv file) is required")
        elif not os.path.exists(os.path.join(base_dir, mp["path"])):
            warnings.append(f"{i}: file '{mp['path']}' not found next to the package")
    return errors, warnings, datasets, models, steps, outputs, mappings


def check_registry(path, known_ids):
    """Verify the forecast registry chain and that forecast inputs are in this package."""
    errors, prev, n_fc = [], "0" * 64, 0
    with open(path, encoding="utf-8") as fh:
        records = [json.loads(line) for line in fh if line.strip()]
    for n, r in enumerate(records, start=1):
        body = {k: v for k, v in r.items() if k != "hash"}
        h = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"),
                                      ensure_ascii=False).encode("utf-8")).hexdigest()
        if r.get("prev_hash") != prev or h != r.get("hash"):
            errors.append(f"registry line {n}: hash chain broken (record altered, removed or reordered)")
            break
        prev = r["hash"]
        if r.get("type") == "forecast":
            n_fc += 1
            for inp in r.get("inputs", []):
                if inp not in known_ids:
                    errors.append(f"forecast {r.get('id')}: input '{inp}' is not in the build index")
    return errors, n_fc


def check_report(path, ids, outputs):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    cited = set(CITE_RE.findall(text))
    errors = [f"report cites unknown id [{c}]" for c in sorted(cited - set(ids))]
    for i, o in outputs.items():
        if o.get("headline", True) and i not in cited:
            errors.append(f"headline output {i} ('{o.get('name')}') is not cited in the report as [{i}]")
    return errors, sorted(cited)


def build(idx, datasets, models, steps, outputs, mappings=None):
    def ref(x):
        return {"@id": x}

    def ent_id(i):
        d = datasets.get(i)
        if d is not None:
            return d.get("path") or d.get("url")
        return "#" + i

    mappings = mappings or {}
    graph = [
        {"@id": "ro-crate-metadata.json", "@type": "CreativeWork",
         "conformsTo": ref(CONFORMS), "about": ref("./")},
    ]
    lic = idx["license"]
    root = {
        "@id": "./", "@type": "Dataset", "name": idx["name"], "description": idx["description"],
        "datePublished": idx.get("datePublished") or date.today().isoformat(),
        "license": ref(lic) if str(lic).startswith("http") else lic,
        "hasPart": [ref(ent_id(i)) for i in datasets] + [ref(mp["path"]) for mp in mappings.values()],
        "mentions": [ref("#" + i) for i in steps],
    }
    # FAIR Signposting relations on the Root Dataset (cite-as /
    # describedby / license). Values come from the build index only:
    # no DOI or licence URL is ever invented here.
    signposting = [{"relation": "describedby", "href": "ro-crate-metadata.json",
                    "type": "application/ld+json"}]
    if idx.get("doi"):
        doi_url = str(idx["doi"])
        if doi_url.startswith("doi.org/"):
            doi_url = "https://" + doi_url
        elif not doi_url.startswith("http"):
            doi_url = "https://doi.org/" + doi_url
        root["identifier"] = doi_url
        signposting.insert(0, {"relation": "cite-as", "href": doi_url})
    if str(lic).startswith("http"):
        signposting.append({"relation": "license", "href": str(lic)})
    root["signposting"] = signposting
    graph.append(root)
    for i, d in datasets.items():
        local = bool(d.get("path"))
        kind = d.get("kind") or ("file" if local else "dataset")
        e = {"@id": ent_id(i), "@type": "File" if kind == "file" else "Dataset",
             "name": d["name"], "identifier": i}
        if d.get("version"):
            e["version"] = d["version"]
        if d.get("version_note"):
            e["description"] = d["version_note"]
        if d.get("retrieved"):
            e["sdDatePublished"] = d["retrieved"]
        if d.get("license"):
            e["license"] = ref(d["license"]) if str(d["license"]).startswith("http") else d["license"]
        if d.get("doi"):
            e["sameAs"] = ref("https://doi.org/" + d["doi"].replace("https://doi.org/", ""))
        graph.append(e)
    for i, m in models.items():
        e = {"@id": "#" + i, "@type": "SoftwareApplication", "name": m["name"],
             "softwareVersion": str(m["version"]), "identifier": i}
        if m.get("url"):
            e["url"] = m["url"]
        graph.append(e)
    for i, s in steps.items():
        e = {"@id": "#" + i, "@type": "CreateAction", "name": s.get("name", i), "identifier": i,
             "instrument": ref("#" + s["instrument"]),
             "object": [ref(ent_id(x)) for x in s.get("inputs", [])],
             "result": [ref("#" + o) for o, out in outputs.items() if out.get("produced_by") == i]}
        if s.get("parameters"):
            e["description"] = f"Parameters: {s['parameters']}"
        if s.get("date"):
            e["endTime"] = s["date"]
        graph.append(e)
    for i, o in outputs.items():
        e = {"@id": "#" + i, "@type": "PropertyValue", "name": o["name"], "value": o["value"],
             "identifier": i}
        if o.get("unit"):
            e["unitText"] = o["unit"]
        if o.get("description"):
            e["description"] = o["description"]
        graph.append(e)
    for i, mp in mappings.items():
        # Semantic mapping set (Round 4 of the v2.7 program, BioDT): one
        # MappingSet entity per mappings.csv, about the dataset it maps,
        # conforming to the SSSOM specification (https://w3id.org/sssom/).
        e = {"@id": mp["path"], "@type": "File", "additionalType": "MappingSet",
             "name": f"Semantic mapping for {datasets[mp['dataset']].get('name', mp['dataset'])}",
             "identifier": i, "about": ref(ent_id(mp["dataset"])),
             "conformsTo": ref("https://w3id.org/sssom/"), "encodingFormat": "text/csv"}
        if mp.get("standard"):
            e["description"] = f"Standard terms: {mp['standard']}"
        graph.append(e)
    return {"@context": CONTEXT, "@graph": graph}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("index", help="build index JSON")
    ap.add_argument("--out-dir", default=".", help="package root; ro-crate-metadata.json is written here")
    ap.add_argument("--check", action="store_true", help="validate only, write nothing")
    ap.add_argument("--report", help="report (markdown/text) whose [out-id] citations are checked")
    ap.add_argument("--registry", help="forecast registry (JSON lines) to tie to this package")
    a = ap.parse_args(argv)
    try:
        with open(a.index, encoding="utf-8") as fh:
            idx = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    errors, warnings, datasets, models, steps, outputs, mappings = validate(idx, a.out_dir)
    cited = None
    if a.report:
        try:
            r_err, cited = check_report(a.report, list(datasets) + list(models) + list(steps) + list(outputs), outputs)
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        errors += r_err
    n_forecasts = None
    if a.registry:
        try:
            g_err, n_forecasts = check_registry(a.registry, set(datasets) | set(outputs))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        errors += g_err
    result = {"index": a.index, "errors": errors, "warnings": warnings,
              "counts": {"datasets": len(datasets), "models": len(models), "steps": len(steps),
                         "outputs": len(outputs), "mappings": len(mappings)},
              "cited_in_report": cited, "registered_forecasts": n_forecasts}
    if errors:
        result["gate"] = "fail"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 3
    if not a.check:
        os.makedirs(a.out_dir, exist_ok=True)
        path = os.path.join(a.out_dir, "ro-crate-metadata.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(build(idx, datasets, models, steps, outputs, mappings), fh, ensure_ascii=False, indent=2)
        result["written"] = path
    result["gate"] = "pass"
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
