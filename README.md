# Burke whistle key attachment

A parametric build123d attachment for a brass high-D Burke whistle. The current
prototype extends the working single key to holes **4, 5 and 6**, with three
independent curved keys, springs and TPU pads.

See the [three-key prototype](docs/three-key-prototype.md),
[assembly STEP](exports/three-key/assembly-open.step), and
[P1S PETG/TPU print project](exports/three-key/whistle-three-key-P1S.3mf).
An [all-PETG dry-fit project](exports/three-key/whistle-three-key-P1S-dry-fit-PETG.3mf)
is also supplied. The new source is [scripts/three_key.py](scripts/three_key.py).

The earlier single-key prototype is retained below for reference.

Start with the [design brief](docs/design-brief.md) for player needs, agreed
hardware, provisional dimensions, manufacturing decisions and trial criteria.
The [acceptance tests](docs/acceptance-tests.md) define engineering assertions
and the usability requirements that need physical trials.

## Single-key print projects

The [all-PETG dry-fit 3MF](exports/single-key/whistle-key-P1S-dry-fit-PETG.3mf)
contains all six pieces on one plate for the P1S, including a rigid pad.
See the [printing notes](docs/printing.md) for orientations, settings and the
separate PETG/TPU version. Open as a project and slice in Bambu Studio.

## Single-key prototype

Edit the parameter block in [scripts/single_key.py](scripts/single_key.py).
Regenerate through the build123d MCP `execute_file` tool, then validate and
export the changed parts. Geometry uses millimetres.

- PETG frame, lever and two identical clamp caps; separate 95A TPU sealing pad.
- Fixed seats for a nominal 2 × 5 mm compression spring, assumed 2 mm solid.
- A 1 × 12 mm steel dowel, friction held in the fixed supports.
- Four M2 bolts and nuts; revised clamps sized for direct contact with brass.
- Low side hinge, curved arm around the tube, reinforced cheeks and a tested
  opening stop; glue-in pad retaining ring and small pin-fit coupon.

The [assembly STEP](exports/single-key/assembly-open.step) is for reviewing the
mechanism. Use the separate files in
[print-oriented](exports/single-key/print-oriented/) for slicing; print two
copies of `clamp_cap_print`. These files have orientations and bed placement,
but do not contain slicer settings or supports.

The [measured tube and hole 4 dimensions](docs/measurements.md) are now applied.
Hole 5 diameter and the remaining reference dimensions are still provisional.
The player confirmed the 1.0 mm pin bore. The first dry fit exposed weak
supports, an ineffective stop and finger obstruction; this curved-arm revision
addresses those findings and needs another physical trial. The player has assembled the spring and hinge and reports that the TPU makes
a reasonable seal. Grip and finger/key clearance failed that trial and are
addressed in the current revision; physical rechecking is still required. CAD validity and
sampled rigid movement checks passed; printability warnings and trial details
are recorded in the brief.

## Earlier layout study

[scripts/whistle_keys.py](scripts/whistle_keys.py), the top-level exports, and
`parameters.json` retain the earlier three-key study. They are not the active
single-key specification. `parameters.json` is an inventory, not model input.
Older concept images may predate manufacturing revisions.

## Build and test

Python 3.12 is used in CI. From the repository root:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/build_ci.py
python -m pytest -q
```

The headless build supplies the inspection helpers normally provided by MCP and
regenerates the active model into ignored `build/`. Tests check solid validity,
bed placement, clearances at 21 key positions, spring travel, pin fit geometry,
and STEP/STL round trips. They do not establish physical sealing or comfort.

[Build and test CAD](.github/workflows/cad.yml) runs on pushes, pull requests and
manual dispatch. Successful runs publish regenerated CAD files and a geometry
report as a downloadable `whistle-cad` artifact. Both the single-key and current
three-key prototypes are regenerated and tested.

## Titanium machining drawing

The [Draftwright drawing package](drawings/titanium/README.md) contains a
[two-sheet PDF](drawings/titanium/frame-machining-review.pdf), dimensioned DXFs,
a datum-aligned STEP and the Python regeneration script. It is for machining
quotation/review; material grade, metal pin retention and final instrument
measurements must be resolved before cutting.
