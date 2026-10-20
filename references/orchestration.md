# Orchestration, multi-agent work, and red team

A digital twin built by one operator follows Phases 0–6 directly. Larger or
higher-stakes builds run through an orchestrated multi-agent layer defined
here. The layer exists to buy **independence and parallelism** — separate
eyes on calibration, adversarial review of claims — not ceremony. If a build
is small, the layer collapses to one operator plus one red-team pass; it is
never allowed to cost more than the errors it prevents.

## Scale tiers

| Tier | When | Who works | Red team |
|---|---|---|---|
| **S — Single operator** | One domain, monitoring or descriptive build, low-stakes decisions | The operator runs all phases | One independent pass at Gate C (before delivery) |
| **M — Orchestrated specialists** | Multi-domain or multi-source build, predictive claims, client-facing deliverable | Orchestrator + data scout + evidence scout + domain modeler in parallel workstreams; calibration auditor independent of the modeler | Gates B and C |
| **L — Full council** | Regulatory, public-health, large-money, or publicly contested decisions | Tier M plus a heterogeneous council (distinct expert personas per member) for design and scenario decisions | Gates A, B, and C |

The tier is chosen in Phase 0 and recorded in the passport, with its reason.
Escalating a tier mid-build is allowed; silently working above the recorded
tier's discipline is not.

## Roles

Personas are seniority-framed and **distinct per agent** — a shared persona
across agents produces duplicated reasoning and is a defect. Frame each as:
role + seniority + scale + working style (+ a comparative clause for
forecast or strategy work: find analogues in other countries or basins,
extract the pattern, state the conditions under which it transfers).

1. **Orchestrator** — senior environmental systems integrator. Owns the
   passport, the phase gates, task contracts, conflict resolution, and the
   single client-facing voice. Never delegates the two human decisions:
   Phase 0 framing (what decision the twin serves) and the Phase 5
   recommendation sign-off — those stay with the owner.
2. **Data scout** — senior environmental data engineer. Builds the source
   matrix and fall-back hierarchy (Phase 1), runs the data quality gate.
3. **Evidence scout** — senior systematic-review methodologist. Builds the
   evidence inventory via `references/evidence-sources.md`, screens by the
   evidence hierarchy, flags abstract-only claims.
4. **Domain modeler** — senior scientist of the object's domain (limnologist,
   hydrologist, agronomist, air-quality modeler, conservation biologist).
   Builds the state model and indicator selection (Phase 2), drafts
   calibration (Phase 3) and scenarios (Phase 5).
5. **Calibration auditor** — senior environmental statistician, **never the
   modeler**. Designs the hindcast split before fitting, verifies metrics
   against the naive baseline, enforces declared failure thresholds.
6. **Red team** — adversarial reviewer (below). Independent of every role
   whose output it attacks.
7. **Optional specialists** — geospatial/remote-sensing analyst; ELSA and
   stakeholder reviewer for sensitive sites. Added by name in the passport
   when the object needs them, not by default.

## Task contracts

Every agent works from a written contract issued by the orchestrator:

- the slice of the object passport the task serves (boundaries, decision,
  maturity target);
- the inputs provided, by manifest ID — an agent never receives "the whole
  project" by default;
- the required output: artifact type, structure, provenance fields, and the
  explicit instruction to **return gaps, not guesses** — an agent that
  cannot support a value reports it as unmeasured;
- the prohibition list: no client contact, no external publication, no
  precise sensitive-species locations in any output, no threshold without a
  named anchor;
- the acceptance check the orchestrator will run before the output enters
  the build.

Outputs enter the build only through the orchestrator, carrying manifest
IDs. Agent prose without provenance is working notes, not build material.

## Conflict resolution

Agents will disagree. Resolution follows the evidence hierarchy, not votes:

1. direct observations of the object;
2. law, standards, and guidelines of the object's jurisdiction;
3. peer-reviewed evidence, weighted by the hierarchy in
   `references/evidence-sources.md`;
4. model output, weighted by its verification scores;
5. agent judgment.

The orchestrator records each material disagreement, the tier that decided
it, and the rationale, in the provenance log. A disagreement that no tier
can settle becomes a stated uncertainty in the deliverable — never a silent
majority decision about a fact.

## Independence rules

- The calibration auditor is not the modeler; the red team is not the
  builder of anything it attacks; where models differ per role, the
  red-team model differs from the arbiter/orchestrator model.
- Personas are distinct per agent (see Roles). One shared persona across a
  council voids the run's value: redo with distinct lenses or downgrade
  the tier honestly.
- The red team sees the artifact and its provenance, not the builder's
  intentions or excuses. Context that would soften the attack is withheld
  until the attack is recorded.

## Red-team gates

The red team's job is to attack the twin the way a hostile reviewer, a
regulator, or reality would. Each attack is recorded with severity
(critical / material / minor), the evidence demanded, and its disposition:
**fixed**, **claim narrowed**, or **risk accepted with owner sign-off**.
An unresolved critical attack blocks the gate.

**Gate A — design (after Phase 2; Tier L, optional in M).** Attacks:
indicators without sources or methods ("indicator theater"); thresholds
imported without a jurisdiction check ("threshold smuggling"); satellite
proxies presented as measurements; missing upstream catchment or airshed
boundaries; state variables that no data stream can feed; maturity target
above what the data inventory can support; sensitive-species leakage paths
in planned outputs.

**Gate B — calibration (after Phase 3; Tiers M and L).** Attacks: tuning on
the scoring data; naive baseline missing or cherry-picked; metric shopping
(reporting only the flattering metric); an assimilation method named
without the data density it requires ("assimilation theater"); failure
periods omitted; uncertainty absent from forecast outputs; a failed
calibration silently re-scoped instead of narrowing the twin's claims.

**Gate C — delivery (before Phase 6; all tiers).** Attacks: scenario
cherry-picking; scoring weights moved after results were seen; nature-based
options skipped without the passport record; an engineered recommendation
without its burden-of-justification statement; headline numbers without
manifest IDs; claims above the declared maturity level; decision-value
claims for a twin that has not yet informed a decision; client conflict of
interest not disclosed; precise sensitive locations anywhere in the package.

A build that passes all gates has earned its claims. A build that cannot
pass ships narrower claims — the red team's product is honesty, not delay.

## Cost and effort discipline

- Agents are convened per phase or per gate, not kept running. Every
  multi-model run is a recorded cost in the project log.
- Tier S is the default. Multi-agent overhead is justified by stakes,
  domains in play, or predictive claims — never by the availability of the
  tooling.
- A red-team pass is the last element cut from a budget and the first
  restored: a small build can skip specialists, but shipping unreviewed
  claims is how twins become score theater.

## Implementation note

The council mechanics in this reference can be implemented with any
multi-model runner that supports: an explicitly chosen model set (never
silent defaults), a distinct persona per council member, and a red-team
pass executed by a model different from the arbiter's. The operator's own
standing rules for which runs are worth their cost govern whether a run
happens; this reference governs what the roles owe each other once it does.
