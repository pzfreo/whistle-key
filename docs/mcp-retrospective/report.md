# Field report: assistive whistle-key CAD workflow, printability checks and a misleading tip-over result

## Outcome

build123d-mcp helped turn an assistive tin-whistle key mechanism into a parameterised, printable assembly through repeated physical prototypes. Its strongest contribution was keeping geometry available for execution, measurement, inspection and export while the design changed. The user reported that the assembled spring and hinge worked and that the TPU pad made a reasonable seal.

The important limitation was the gap between valid CAD and a usable manufactured part. Several problems were discovered by the user handling printed parts: weak frame transitions, finger interference, key/frame catching, inadequate clamp tightening clearance and an unsuitable print orientation after a design change. These are failures of our design and verification coverage; they are not evidence that the CAD server produced invalid geometry.

This report includes a retrospective experiment with `analyze_printability`. It correctly identifies the old clamp's unsupported surface, but reports a questionable tip-over error for the corrected clamp. That is the main new actionable finding. Other suggestions below link existing issues rather than claiming previously unreported omissions.

## Environment and evidence

Reported by the running server on 9 September 2026:

| Component | Version |
|---|---|
| build123d-mcp | 0.3.84 |
| build123d | 0.11.1 |
| build123d-drafting-helpers | 0.14.2 |
| bd_warehouse | 0.3.0 |
| augura | 0.1.7 |

Project: [pzfreo/whistle-key](https://github.com/pzfreo/whistle-key). The mechanism uses PETG structural parts, TPU pads, steel hinge pins, compression springs and M2 fasteners around a cylindrical brass whistle. Development progressed from one key to three interchangeable keys and pads.

Reproducible geometry:

- [Old print-oriented clamp STEP, cbce323](https://github.com/pzfreo/whistle-key/blob/cbce323/exports/three-key/print-oriented/clamp_cap_print.step).
- [Corrected print-oriented clamp STEP, d6b1df1](https://github.com/pzfreo/whistle-key/blob/d6b1df1/exports/three-key/print-oriented/clamp_cap_print.step).
- [Corrected clamp image](https://raw.githubusercontent.com/pzfreo/whistle-key/d6b1df1/docs/clamp-cap-flat-end.png).
- [Canonical generation source](https://github.com/pzfreo/whistle-key/blob/d6b1df1/scripts/three_key.py) and [project assertions](https://github.com/pzfreo/whistle-key/blob/d6b1df1/tests/test_three_key.py).
- [Captured analysis evidence](https://github.com/pzfreo/whistle-key/blob/main/docs/mcp-retrospective/printability-evidence.json).

The versions above describe the retrospective run, not necessarily every server used during the project's history.

## What worked well

**Source-backed iteration.** Executing the repository's Python source and retaining named geometry made repeated changes practical. Parameters for hole spacing, pad size, pin clearance and frame geometry could feed the same generation workflow. Keeping the repository source authoritative matters: a successful interactive experiment alone is not a reproducible deliverable. This experience supports [#443](https://github.com/pzfreo/build123d-mcp/issues/443).

**Numerical checks alongside visual inspection.** Measurements, validity checks and exports gave concrete evidence about the result of edits. Renders helped communicate changes, while STEP files let the user inspect assemblies and individual parts. Neither a convincing render nor a successful export establishes finger clearance, clamp grip or support-free printing.

**Independent verification of drawing geometry.** During a separate Draftwright evaluation, a true section through the titanium frame reference measured 101.67622552458513 mm² in the MCP session. That agreed with the corrected drawing hatch area, approximately 101.676225524572 mm², and helped distinguish the intended section from incorrectly included geometry. See [drawing checks](https://github.com/pzfreo/whistle-key/blob/76ccdc2/drawings/titanium/drawing-checks.json) and [Draftwright report #1529](https://github.com/pzfreo/draftwright/issues/1529). The drawing defects belong to Draftwright; build123d-mcp was useful as an independent checker.

**A platform for engineering assertions.** We authored checks for key travel, frame and clamp clearance, pad seating, interchangeability and the clamp's first-layer connectivity. These are project-specific assertions built on CAD operations, not requirements automatically inferred or certified by MCP. Physical testing remained necessary for force, grip, sealing and usability.

## What went badly: we skipped an available printability check

The old clamp had a 4 mm-wide curved band between 6 mm-wide fastening tabs. In its supplied print orientation, the tabs touched the bed but the curved band began 1 mm above it. Validity and assembly checks did not catch that manufacturing problem.

The correction shortened the bed-facing tab extensions so the band and tabs begin on the same plane. The resulting cap has a connected C-shaped first-layer footprint.

An important correction to the initial retrospective: **`analyze_printability` already exists. We did not invoke it before delivering the problematic clamp.** Running it afterwards with a `256 256 256` build volume and other parameters at their defaults produced:

| Finding | Old cap | Corrected cap |
|---|---|---|
| Overhang | Warning: 98.1 mm² flat ceiling, 13.1 mm span; location Z ≈ 1 mm | No overhang finding |
| Tip-over | Error; projected centre of mass outside reported footprint | Error; projected centre of mass outside reported footprint |

The overhang result is a clear success for the existing tool. Our workflow should have run it on the actual exported print orientation before delivery. Absence of an overhang finding is still not a guarantee that every printer and slicing configuration will succeed.

## New finding: corrected curved cap gets a questionable tip-over error

For the corrected cap the tool says:

```text
Centre of mass (-0.0, 0.8) projects outside the bed-contact footprint; the part will topple
```

The finding has `kind: tip_over`, `severity: error`, and null `area` and `location`.

We independently reconstructed the static support polygon from the bed-contact geometry. Bed faces were selected where both minimum and maximum Z were within 1e-6 mm of zero. A convex hull made using only topological vertices excludes the lower extrema of the curved edges. Sampling each contact edge at 33 parameter positions captures those curves:

| Measurement | Old cap | Corrected cap |
|---|---|---|
| Bed-contact faces | 2 | 1 |
| Projected centre of mass, Y | 1.27956 mm | 0.83773 mm |
| Vertex-only hull contains projected COM | No | No |
| Sampled contact hull Y extent | 4.775 to 8.275 mm | −8.275 to 8.275 mm |
| Sampled contact hull contains projected COM | No | Yes |

The corrected cap's projected centre of mass lies inside the convex hull of actual sampled contact points. A C-shaped footprint can support a centre of mass projected into its open region; static stability depends on the support polygon, not simply whether that point lies in contact material.

This contradicts the categorical geometric explanation for the corrected cap. A vertex-only hull or a footprint-membership test is a possible explanation, **not a confirmed implementation diagnosis**: we have not inspected the analyzer's source to establish the cause. This should be investigated in the MCP/augura analysis path.

No physical stability experiment was performed for this retrospective. Adhesion, nozzle forces and printing dynamics remain separate concerns even when the static support-polygon test passes.

### Reproduction

Download the two linked STEP files and execute in the MCP session:

```python
from build123d import *
old_cap = import_step('/absolute/path/cap-before.step')
new_cap = import_step('/absolute/path/clamp_cap_print.step')
show(old_cap, 'review_old_cap')
show(new_cap, 'review_new_cap')
```

Then call `analyze_printability` once per object:

```json
{"object_name":"review_old_cap","build_volume":"256 256 256"}
```

```json
{"object_name":"review_new_cap","build_volume":"256 256 256"}
```

For the independent check, collect the coplanar Z=0 faces, sample each edge with `edge.position_at(i / 32)` for `i` from 0 through 32, compute their 2D convex hull, and test `part.center(CenterOf.MASS)` projected into XY against that hull. The captured evidence includes both the vertex-only and sampled results.

## Other friction and opportunities

**Structured results and output size.** Some results put prose and serialised JSON inside a string, alongside text and structured wrappers. That creates extra parsing work and makes it easy to repeat large outputs. Our orchestration also amplified this by displaying entire response objects. Compact typed results with optional detail would help; relevant existing work is [#449](https://github.com/pzfreo/build123d-mcp/issues/449), [#370](https://github.com/pzfreo/build123d-mcp/issues/370) and [#437](https://github.com/pzfreo/build123d-mcp/issues/437).

**Optional capability discovery.** Server instructions advertised Draftwright as importable, but it was absent from the execution environment. We used a separate local environment for the drawing workflow. This is already tracked in [#475](https://github.com/pzfreo/build123d-mcp/issues/475); the desired improvement is accurate optional-package discovery and conditional guidance, not mandatory installation. Package/source introspection also encountered sandbox restrictions. A supported capability/version interface is preferable to weakening the sandbox.

**Actionable diagnostic evidence.** A tip-over finding should expose its assumed bed plane, contact region or hull, projected centre of mass and geometric margin. A render overlay would make a disagreement much easier to resolve. Related diagnostic-location concerns exist in [#436](https://github.com/pzfreo/build123d-mcp/issues/436), although that issue concerns thin walls rather than this support-polygon example.

**Separate validation results.** Workflow guidance should distinguish solid validity, assembly clearance, printability in the final orientation, and user-defined engineering requirements. A single successful validity result must not imply all four passed. Named object identity and the exact analyzed/exported orientation should remain explicit so checks apply to the delivered geometry.

## Suggested priorities and acceptance criteria

1. **Investigate the curved-contact tip-over result.** Add the corrected cap as a regression fixture. Include curved contact boundaries in the support calculation and report the actual geometric evidence. If another criterion triggers the error, explain it rather than asserting that the projected centre of mass lies outside its support polygon.
2. **Make existing printability analysis a routine delivery step.** Guidance should call it on print-oriented parts and review unresolved findings before export delivery. The old cap should retain its Z≈1 mm overhang warning; the corrected cap should not have that same warning. This is a workflow improvement, not a request for a new analyzer.
3. **Expose useful diagnostic geometry.** Return the support hull, projected centre of mass and assumptions in typed data, ideally with an optional annotated view. Avoid an unconditional prediction of toppling where the analysis is heuristic or incomplete.
4. **Continue existing capability and response-schema work.** Link this report as evidence for #475 and #449 rather than opening duplicate requests.

The overall assessment is positive: the server made iterative CAD and independent checks practical. Its value increases when available analysis tools are actually used, results identify their assumptions, and project-specific engineering requirements remain explicit. The physical prototypes exposed gaps that valid solids and attractive renders could not settle.
