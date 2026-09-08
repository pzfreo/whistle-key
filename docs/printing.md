# Printing the single-key prototype

## All-PETG dry fit

Open [`whistle-key-P1S-dry-fit-PETG.3mf`](../exports/single-key/whistle-key-P1S-dry-fit-PETG.3mf)
as a project in Bambu Studio. This is the player's requested dry run: all six
pieces are PETG, including the normally flexible pad.

The single plate contains one frame, one key, two identical clamp caps, one
rigid pad and one pin-fit coupon. Each mesh is already oriented and on the bed.
The project selects a P1S with a 0.4 mm nozzle and Generic PETG. Confirm the
actual filament profile and build plate, then slice and inspect the preview.
No G-code is embedded. Do not auto-orient the parts again.

Settings stored in the project:

- 0.16 mm layers, four walls, five top and bottom layers.
- 25% infill for rigid parts; solid infill for the pad.
- Automatic normal supports enabled for the frame and curved key.
- 3 mm outer brims for the frame and clamp caps.

The frame rests on its outer rail side. The key is finger-face down, with its pad ring and
curved arm upwards; inspect supports beneath its hinge and spring peg. Caps stand on flat end faces. The pad sits on its
flat back; the curved contact face points up. The coupon sits on its flat base.

## PETG and TPU version

[`whistle-key-P1S.3mf`](../exports/single-key/whistle-key-P1S.3mf) keeps the same
orientation, using three plates: PETG pin-fit coupon, PETG mechanism parts, and
TPU pad. The TPU pad has a 0.12 mm layer-height override and solid infill. Use
external feeding for ordinary 95A TPU and select settings for the actual filament.

## Packaging and verification

The packager reads existing oriented STL exports. It does not redesign or
rescale them. The 3MF is read back with lib3mf and checked for mesh integrity,
quantities, material assignments, bed height, unaltered orientation and spacing.
The package was not opened or sliced in Bambu Studio in this environment: its
GUI executable could not run because required system libraries were unavailable.
The slicer preview remains the final check for support placement and settings.

Regenerate from the repository root:

```sh
python scripts/package_3mf.py
python scripts/package_3mf.py --dry-run --output exports/single-key/whistle-key-P1S-dry-fit-PETG.3mf
```

CI packages both versions from freshly regenerated meshes and tests their
contents. JSON files alongside the projects record part/plate assignments and
bounding boxes. Bambu project metadata follows the application's
[3MF importer](https://github.com/bambulab/BambuStudio/blob/v02.08.02.61/src/libslic3r/Format/bbs_3mf.cpp)
and plate layout conventions.

The lowered clamp-joint revision requires the new frame and both new caps. The key, pad and pin are reusable.

The subsequent full-width pillar reinforcement changes only the frame; reuse the lowered-joint caps and the existing key and pad.

The joined clamp base and enlarged spring peg revision requires a new frame and key. Reuse the current caps and pad; trial the larger peg in the actual spring.

The rounded arm-shoulder revision changes only the key. Reuse the joined-base frame and current caps and pad.

The next friction-fit trial uses 1.1 mm fixed hinge bores with the existing 1.0 × 12 mm steel pin. The moving key bore remains 1.25 mm. This supersedes the 1.0 mm frame bore for the next print; retention is not yet confirmed. Only the frame changes.

The joined-pillar pedestal revision changes only the frame, retaining the 1.1 mm fixed-bores trial. Reuse the current key, caps and pad.

The bare-brass fit and finger-clearance revision requires a new frame and both caps. Fit without a liner. Reuse the key, pin, spring and TPU pad; verify grip before playing.

For the three-hole extension, use the separate [three-key printing and assembly instructions](three-key-prototype.md) and files under `exports/three-key/`.

The three-key frame now has an opposite-side rail and a third clamp between keys 5 and 6. Print its frame flat on the base as supplied, and print three identical caps. It uses six M2 bolts/nuts. The updated projects include all eleven pieces.

The M2 nut-pocket revision changes only the three-key frame. Fit six nuts from underneath after clearing any pocket supports; hex pockets resist rotation while tightening. Current defaults are 4 mm across-flats nuts, 1.6 mm thick. Existing caps, keys and pads remain usable.
