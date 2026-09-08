# Titanium frame — machining review P1

This package describes the existing three-key lower frame for a CNC machining
quotation and design-for-manufacture review. It is **not released for cutting**.
The titanium grade, metal hinge-pin retention, cutter access/internal radii,
and the player's hole 5/6 measurements remain unresolved. No supplier has been
contacted and no machining order has been placed.

The frame is a 3D milled/drilled component, not a flat laser/waterjet profile.
Its nominal envelope is **31.300 × 71.595 × 15.300 mm**. The 3.5 mm base is only
one level; raised bearings and spring housings are integral. Stock allowance
and workholding must be chosen by the machinist.

## Package

- `frame-machining-review.pdf`: combined two-sheet PDF for sharing.
- `frame-general.pdf`: orthographic/isometric views, envelope dimensions,
  proposed machining notes and release holds.
- `frame-features.pdf`: coordinate schedule, hole callout and functional sizes.
- Matching SVG and DXF files are drawing sheets, **not cutting toolpaths**.
- `frame-reference.step`: exact nominal geometry for CAM review. No titanium
  redesign or tool-radius compensation has been applied.
- `drawing-checks.json`: version/hash provenance and Draftwright diagnostics.
- `../../scripts/draw_titanium_frame.py`: reproducible Draftwright Python source.

The STEP is the committed PETG frame translated into a machining coordinate
system: X=0 is the whistle centreline, Y=0 the foot-end clamp centre and Z=0 the
flat underside. +Y points towards the mouthpiece; +Z towards the whistle.
Relative to `frame_print.step`, the translation is (0, 32.2975, 0) mm. Its shape
and volume are unchanged. Dimensions are in millimetres; do not scale a drawing.
Use the STEP for unlisted contours, with the drawing's fit notes and release
holds. Coordinate locations are nominal, not a claim that the instrument has
been measured to three decimal places.

## Manufacturing decisions to resolve

1. **Pin retention.** The 1.10 mm fixed bores were a PETG print-fit experiment.
   A machined 1.10 mm bore and 1.00 mm pin have 0.10 mm diametral clearance.
   Do not call this a press/friction fit. Agree bore limits and retention using
   the actual pins before revising the CAD. Preserve access for pin insertion.
2. **Nut pockets and internal corners.** The six 4.30 mm AF hex pockets have
   sharp nominal corners. Ordinary end milling leaves internal radii; the
   shop must propose corner relief or a suitable secondary process. Relief
   must preserve the nut-bearing flats, 1.6 mm roof and surrounding wall.
   This follows [Protolabs' CNC milling guidance](https://www.protolabs.com/services/cnc-machining/cnc-milling/design-guidelines/).
   Other sharp internal intersections also need cutter-access review; no blanket
   permission to add radii in moving-key clearances is given.
3. **Small cross holes and blind seats.** Six coaxial bearing bores run along Y.
   Three 2.4 mm spring sockets run along X and require a flat floor at full
   specified depth. A standard drill-point depth is not interchangeable with
   the 1.5 mm cylindrical spring seat. Inspect access and fixturing from both
   sides, underside and above.
4. **Whistle fit.** Three R7.15 seats share an axis. The 14.2 mm brass whistle,
   existing PETG caps and 1.2 mm nominal split gap are the starting interfaces.
   A geometric tightening allowance alone does not establish titanium clamp
   grip or acceptable pressure on the brass. Trial the metal assembly.
5. **Measurements and material.** Key 5/6 dimensions are being rechecked.
   Confirm these before fixing pedestal positions. Titanium grade and condition
   are not assumed. Tolerances and surface finish on the drawing are proposals
   for review, not measured or supplier-approved capability.

## Regeneration

Use a separate environment: the CAD project's tests use build123d 0.11.0,
whereas the inspected Draftwright version requires build123d below 0.11.

```sh
python -m venv /tmp/whistle-drawing-venv
/tmp/whistle-drawing-venv/bin/pip install -r drawings/titanium/requirements.txt
/tmp/whistle-drawing-venv/bin/python scripts/draw_titanium_frame.py
```

After changing the model, regenerate and datum-align the STEP through build123d
MCP before running the drawing script. The script reads the model parameter
block, checks the source STEP and emits the views through Draftwright. Review
both the machine-readable lint and the rendered PDFs; a clean drawing-layout
report would not release the part for manufacture.

## Drawing review and limitations

The fully automatic first pass reported dropped bore callouts and was stopped
after repeated layout retries. The refined version explicitly declares separate
bolt, spring and hinge hole groups and uses a coordinate table. This avoids
conflating the six vertical 2.4 mm bolt holes with the three horizontal 2.4 mm
blind spring sockets. It also adds a clamp section and shorter title-block text.

Visual inspection exposed two section-renderer issues in the pinned Draftwright
revision: rear-facing surfaces behind the section plane were hatched, and the
cut indicators pointed opposite the rendered +Y viewing direction. The drawing
script contains a narrowly scoped workaround: hatch only faces lying on the
specified cutting plane, and orient the indicators into the retained half.
It records hatch-face areas and excluded uncut faces for inspection. No manual
page coordinates are used to relocate views or dimension labels.

Draftwright still reports unsupported hex-pocket grammar and incomplete or
unverifiable feature provenance. Those warnings are retained in the JSON files;
the package does not claim automatic completeness. The coordinate and feature
notes supplement the views, and the STEP carries the remaining contours.
Independent assertions check actual cylindrical surfaces (counts, centres,
axes and depths), all 36 nut-pocket walls, and preservation of the original
frame geometry under translation. These are geometry checks, not validation
of metal friction fits, stiffness or manufacturing capability.
