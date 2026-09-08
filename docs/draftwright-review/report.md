# Field report: titanium-frame drawing — section correctness, hole semantics, documentation and iteration

Draftwright produced a useful two-sheet machining-review package from a real, moderately complex STEP model. Its domain-level authoring, repeated-hole callouts, automatic view placement and multi-format export were valuable. However, getting a trustworthy result required visual inspection, independent geometry checks, a private renderer workaround and several API corrections. The most serious problem was a section view that hatched uncut material. A separate lint suggestion would have incorrectly merged two distinct drilling operations.

This report records one practical trial, not a controlled performance benchmark or a claim that every issue affects every model. Suggested priorities below are for triage. It can serve as a parent issue for smaller fixes.

## Task, environment and evidence

The task was to create and improve a technical drawing for a titanium version of a three-key whistle frame. The input remained the nominal PETG prototype geometry: this exercise produced a quotation/design-for-manufacture review, not a released titanium design.

| Item | Trial configuration |
|---|---|
| Date | 2026-09-08 |
| Draftwright | `0.4.25.dev0`, source commit `c365452ac4603f7d86b3c45545ce6c312be4e16b` |
| Python/platform | Python 3.12, Linux x86-64 |
| Drawing environment | build123d `0.10.0`, build123d-drafting-helpers `0.15.1`, Quiddity `0.2.6`, cadquery-ocp `7.8.1.1.post1` |
| Existing CAD project | build123d `0.11.0`; ultimately kept in a separate environment |
| Model | One solid; 210 faces, 597 edges; 31.300 × 71.595 × 15.300 mm |
| Volume | 6313.313392 mm³ |
| Features | Six vertical bolt holes, six horizontal hinge bores, three horizontal blind spring sockets, six underside hex nut pockets, curved whistle seats and raised supports |
| Final output | Two A2 sheets at 2:1 for orthographic views; isometric views marked NTS; PDF, SVG, DXF, STEP and Python source |

Pinned trial artifacts:

- [Datum-aligned STEP](https://github.com/pzfreo/whistle-key/blob/76ccdc2/drawings/titanium/frame-reference.step)
- [Original print-frame STEP used by the automatic first pass](https://github.com/pzfreo/whistle-key/blob/76ccdc2/exports/three-key/print-oriented/frame_print.step)
- [Final Draftwright Python generator, including the workaround and independent checks](https://github.com/pzfreo/whistle-key/blob/76ccdc2/scripts/draw_titanium_frame.py)
- [Combined drawing PDF](https://github.com/pzfreo/whistle-key/blob/76ccdc2/drawings/titanium/frame-machining-review.pdf)
- [Machine-readable checks and lint](https://github.com/pzfreo/whistle-key/blob/76ccdc2/drawings/titanium/drawing-checks.json)
- [Dependency pin](https://github.com/pzfreo/whistle-key/blob/76ccdc2/drawings/titanium/requirements.txt)
- [Automatic-pass interruption log](https://github.com/pzfreo/whistle-key/blob/186c895/docs/draftwright-review/automatic-first-pass.log)

The final package is explicitly marked **QUOTATION / DFM REVIEW — NOT RELEASED**. Titanium grade, metal pin retention, internal-corner machining and final instrument measurements were not settled. Those are engineering inputs; Draftwright should not invent them.

## What went well

### 1. Useful views from the actual solid

Orthographic and isometric views made the frame understandable. The final layout also accommodated a clamp section, coordinate schedule and substantial machining notes. This was much better than manually tracing a raster image or reconstructing the shape as a drawing.

### 2. Domain-level authoring was a productive fallback

After the fully automatic approach struggled, `Sheet`, `envelope()`, `hole()`, `dimension()`, `table()` and `notes()` let us state the required information while leaving placement to the engine. We did not manually place the principal views or ordinary dimension labels.

The successful feature sheet separates:

- **6 × Ø2.4 through bolt holes**, axis Z;
- **3 × Ø2.4 blind spring sockets**, axis X, 1.5 mm full-diameter depth;
- **6 × Ø1.1 nominal hinge bores**, axis Y, with the metal fit explicitly on hold.

![Final feature sheet](https://raw.githubusercontent.com/pzfreo/whistle-key/186c895/docs/draftwright-review/feature-sheet.png)

The coordinate schedule was particularly useful: this frame has repeated features along different axes, and placing every coordinate as a separate dimension would make the sheet harder to read.

### 3. Diagnostics exposed uncertainty

The reports retained unsupported and unverifiable requirements instead of treating them as fully covered. In particular, six hexagonal blind recesses were identified as unsupported by the current drafting grammar. The distinction between legibility, fidelity and completeness is useful, and the detailed reasons are worth preserving.

### 4. Export and reproducibility worked

PDF, SVG and DXF export all succeeded in the isolated drawing environment. It was practical to retain the generator, source STEP, version pins, hashes and diagnostics alongside the outputs. The final ZIP passed an integrity check and the combined PDF contained the intended two sheets.

### 5. The design-intent boundary remained explicit

The drawing could carry unresolved fits, material and machining notes without making up a titanium grade or claiming that a printed hole allowance was a metal press fit. That is the right outcome for this stage of the design.

## What went badly

### A. High priority: section hatching included material behind the cut plane

**Confirmed on the fixture, visually and by source inspection.**

We requested a section at Y=0 through the foot-end clamp. The generated section hatched raised hinge-support faces farther along Y, although those faces were not intersected by that plane. This changes what the drawing says about the part; it is not merely cosmetic.

The relevant selection in [sections.py at the tested revision](https://github.com/pzfreo/draftwright/blob/c365452ac4603f7d86b3c45545ce6c312be4e16b/src/draftwright/annotations/sections.py#L412) is:

```python
cut_faces = [f for f in keep_behind.faces() if f.normal_at().Y < -0.9]
```

That selects faces by orientation, without requiring them to lie on the cutting plane. Rear-facing surfaces on retained features therefore enter the hatch set.

**Before:** uncut supports are hatched.

![Before section correction](https://raw.githubusercontent.com/pzfreo/whistle-key/186c895/docs/draftwright-review/section-before.png)

**After the local correction:** only material intersected by Y=0 is hatched; retained features behind it remain visible but unhatched.

![After section correction](https://raw.githubusercontent.com/pzfreo/whistle-key/186c895/docs/draftwright-review/section-after.png)

The bounded workaround filtered candidate hatch faces to those whose Y bounds both match the cut plane within tolerance. For this fixture it:

- excluded **17 uncut faces**;
- retained **3 actual cut faces**;
- produced total cut-face area **101.676225524572 mm²**;
- matched an independent build123d section, **101.676225524585 mm²**, within 1e-5 mm².

This workaround is evidence, not a proposed universal API or complete treatment of arbitrary section geometry. The upstream fix should use reliable cutting-plane/intersection provenance.

**Requested regression:** place raised rear-facing features behind, but not on, a section plane. Assert their faces are not hatched; compare the hatched region with the actual section region, including voids. Check more than screenshots and normal directions.

### B. High priority: section indicators opposed the rendered viewing direction

**Observed and supported by the renderer implementation for this fixture.**

The renderer removes the lower-Y half and places the camera at lower Y looking toward the retained positive-Y half. The plan-view indicators were constructed with `tip_y = y_page - wing_h` and `rotation=-90`, pointing in the opposite direction on this drawing.

The local correction points them into the retained half. Relevant source is [the section camera and arrow construction](https://github.com/pzfreo/draftwright/blob/c365452ac4603f7d86b3c45545ce6c312be4e16b/src/draftwright/annotations/sections.py#L393).

**Requested regression:** verify the section plane, removed half, retained half, camera direction and projected indicator vectors as one contract. Exercise first- and third-angle layouts, with an asymmetric part so a reversed view is observable. The local trial covered third angle only.

### C. High priority: a lint fix merged different operations solely because their diameters matched

**Observed in an intermediate feature-sheet diagnostic.**

With the six bolt holes declared, lint said:

```text
9 ø2.4 features on the part but callouts account for 6
```

Its suggested fix was to set the callout count to nine. But the other three features are blind spring sockets along X; the six bolt holes are through holes along Z. Changing the bolt callout to `9× Ø2.4 THRU` would be false.

We instead declared a separate three-socket group. The count warning then disappeared while retaining the two different operations. The diameter-only suggestion is also visible in [linting/suggest.py](https://github.com/pzfreo/draftwright/blob/c365452ac4603f7d86b3c45545ce6c312be4e16b/src/draftwright/linting/suggest.py#L55).

**Requested improvement:** preserve axis, through/blind status, depth and occurrence ownership in count reconciliation and suggestions. When diameters match but operations differ, identify the unclaimed occurrences and propose a separate group. Do not issue a mechanically applicable count change that alters manufacturing meaning.

### D. Medium priority: the automatic first pass was slow and opaque

The first pass used `build_drawing()` with A2, requested scale 2, third-angle projection and automatic dimensions. It repeatedly printed:

```text
plan/side right strip: 1 of 2 bore callouts skipped (strip full)
```

It ran for several minutes without delivering its first exported sheet and was interrupted. **This does not prove an infinite loop or establish a runtime benchmark.** We did not profile every stage, and other local work was running during part of the trial.

The interruption stack was in leader placement/materialization, specifically `_rendered_ink_matches()` → `_validated_face_mesh()` → edge enumeration. It would be inaccurate to attribute this incident solely to exact HLR.

**Requested improvements:** stage-level progress and elapsed times, candidate/scale retry reporting, a bounded search budget, and retention of the best diagnostic result on cancellation. Profile annotation ink materialization as well as projection. Related: #1137 and #1228, but this is not evidence of the same root cause as either.

### E. Medium priority: the skill and section API did not line up cleanly

The inspected skill teaches `Sheet.section()`. The implementation warns that it is deprecated and recommends `add_section_view()`/`section_view()`.

Trying `add_section_view('A', at=0)` on an explicitly authored sheet then failed with:

```text
augment automatic derived views; call auto_views() first
```

Adding `auto_views()` succeeded, but produced a soft-deprecation warning recommending `authored_views()` plus explicit view declarations. That warning is not a removal notice; nevertheless, the discovery path was unnecessarily circuitous.

There was also an operator error: `s.dimension(bolt, 'diameter')` failed because the Sheet measurement ID is `bore.diameter`. The exception helpfully listed valid measurements. The skill does explain that `Drawing.dimension()` and `Sheet.dimension()` use different spellings, so this is not wholly a documentation failure.

**Requested improvements:** test the skill's examples against the shipped package; include a complete current example combining authored dimensions with a section; demonstrate hole `bore.diameter` and `dimension_ids()` explicitly. This is related to the already-closed #988, with a different remaining section-workflow mismatch.

### F. Medium priority: completeness does not reconcile the two-sheet package and its notes well

Final recorded results:

| Metric | General sheet | Feature sheet |
|---|---:|---:|
| Errors | 0 | 0 |
| Warnings | 35 | 36 |
| `passed` | true | true |
| Overall `score` | 0.0 | 0.0 |
| Legibility score | 1.0 | 1.0 |
| Recognized requirements in audit | 58 | 58 |
| Requirements placed | 0 | 2 |
| Satisfied by structured note | 0 | 0 |
| Unsupported | 6 | 6 |
| Unverifiable | 52 | 47 |

The feature sheet additionally reported three suppressed requirements. We are not treating those as valid coverage simply because the drawing looked readable.

Some general-sheet warnings are expected: the drill information deliberately lives on sheet 2. The feature notes also state pocket AF/depth, socket depth, bearing spans and seat sizes, but ordinary free-text notes do not establish structured requirement ownership. It is reasonable not to infer semantic coverage from arbitrary prose.

The problem is the workflow gap: after doing the sensible human thing—split the information across sheets and use a feature schedule—the report still needs extensive manual interpretation. An extra `repair()` left both final summaries unchanged; it did not resolve this semantic gap, nor should we expect a layout repair to invent feature provenance.

**Requested improvements:** package-level requirement ownership, supported feature-linked schedules/notes, and a concise distinction between layout validity, geometry coverage, fidelity uncertainty and missing manufacturing decisions. `passed=true` beside a zero score and dozens of warnings needs an immediately visible explanation. Do not make the score greener by suppressing unsupported requirements.

The feature sheet also retained two `diameter_leader_target_unverifiable` warnings. We visually inspected the leaders and independently checked the bores, but that is not a complete automated proof of leader-to-boundary fidelity. Those warnings should remain actionable, with feature/view identity and a highlighted target preview.

### G. Lower priority: presentation and export needed polish

The initial long material field was crowded in the title block. Shortening it to `Ti / TBD` improved the output. It would be better for title-block fields to fit, wrap or report overflow explicitly.

The A2 pages were readable but left substantial unused space while the note blocks were relatively small. A layout preference for larger notes or a more compact sheet would help. This is an editorial observation, not proof that the optimizer chose the wrong feasible layout.

The final DXFs were approximately **8.55 MB and 8.74 MB**, with SVGs around **1.48 MB and 1.52 MB** and PDFs around **0.56 MB each**. Generated drawing files created extremely noisy repository diffs until marked as generated/binary for review. Compact export options and documented Git attributes would help; this trial did not isolate which entities dominate size.

## Environment problems: distinguish integration from our mistakes

The available CAD MCP server advertised Draftwright as importable, but `import draftwright` returned `ModuleNotFoundError`. We therefore ran Python locally against the verified STEP. This was an integration/deployment mismatch, not proof of a Draftwright import defect.

We initially installed Draftwright into the CAD project's existing virtual environment. That was our mistake. The declared dependency correctly selected build123d below 0.11, downgrading the project's version. Restoring build123d then exposed overlapping OCP distributions until the original OCP packages were restored. The successful approach was a separate drawing environment.

Suggested improvement: a short preflight that reports package presence, kernel/dependency compatibility and the intended execution environment before a CAD-to-drawing workflow starts. Document the isolated-environment route prominently while supported versions differ.

## Reproduction

For the full corrected package and independent checks:

```sh
git clone https://github.com/pzfreo/whistle-key.git
cd whistle-key
git checkout 76ccdc2
python -m venv /tmp/whistle-drawing-venv
/tmp/whistle-drawing-venv/bin/pip install -r drawings/titanium/requirements.txt
/tmp/whistle-drawing-venv/bin/python scripts/draw_titanium_frame.py --verify-only
/tmp/whistle-drawing-venv/bin/python scripts/draw_titanium_frame.py
```

A reduced fixture-based reproduction for the unpatched section renderer is below.
It uses the same section request and input as the observed failure, but omits the
notes and tables; this reduced snippet has not been separately run. The archived
before/after images and source inspection are the evidence from the actual run.

```python
from build123d import import_step
from draftwright import Sheet

part = import_step('drawings/titanium/frame-reference.step')
s = Sheet(part, title='CLAMP SECTION REPRO', number='REPRO-1',
          page='A2', scale=2, projection='third',
          tolerance='REVIEW ONLY', detail_view=False)
env = s.envelope(part)
for parameter_id in env.dimension_ids():
    s.dimension(env, parameter_id)
s.auto_views()
s.add_section_view('A', at=0.0)
d = s.build()  # No consumer-side corrected_section() patch.
d.export('build/section-repro', formats=('svg', 'pdf'))
```

The original automatic call, before the domain-authored fallback, was:

```python
from draftwright import build_drawing

d = build_drawing(
    'exports/three-key/print-oriented/frame_print.step',
    title='THREE-KEY FRAME - TITANIUM REVIEW',
    number='WK-TI-001', material='TITANIUM - GRADE TBD',
    tolerance='SEE REVIEW NOTES', page='A2', scale=2,
    projection='third', date='2026-09-08', revision='P1',
    reproducible=True,
)
```

The independent checks validated cylinder counts, centres, axes and depths; all 36 hex-pocket walls; preservation of original frame geometry under translation; and the corrected section area. These checks do **not** prove all dimensions are present, all leaders are faithful, or the design is ready to manufacture. The CAD repository's CI also passed, but it is not a Draftwright acceptance test.

## Suggested follow-up order and acceptance criteria

1. **Section correctness:** reproduce A/B, fix cut-face selection and indicator direction, and add geometric regression assertions before more layout polish.
2. **Safe count suggestions:** add this mixed-axis, mixed-depth Ø2.4 fixture; never suggest a false nine-through-hole operation.
3. **Public review workflow:** make feature provenance, unsupported geometry, retained warnings and package-level ownership straightforward to inspect. Build on the existing contracts in #1256 rather than introducing another parallel report model. Its current checkpoint already records delivered inspection/report work; this trial did not evaluate all of it.
4. **Skill/API consistency:** execute the documented examples in CI, including a section on an authored sheet, and keep migration advice consistent.
5. **Iteration cost:** instrument this fixture, separate recognition/projection/placement/ink-check/lint/export costs, and return bounded, useful results when automatic placement struggles.
6. **Shop-package usability:** improve title-block fitting, note legibility, artifact manifests and export size. Keep preliminary status distinct from manufacturing release.

The core approach worked: the final drawing communicated a difficult little frame well. The next improvement should make that result trustworthy through supported APIs and geometric evidence, without requiring a consumer to patch private section-rendering functions.
