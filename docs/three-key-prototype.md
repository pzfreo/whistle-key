# Measured three-key prototype

The working hole-4 mechanism is extended to holes 4, 5 and 6 on one 70.595 mm
frame. Each curved key has its own normally open coil spring, 1 × 12 mm steel
pin and glued concave TPU pad. Hole 4's key and pad geometry is retained;
holes 5 and 6 have larger pads and cups. All geometry is metric and controlled
by `scripts/three_key.py`.

## Measurements and pad sizes

Bottom edges are independently measured from the whistle foot; centres are
derived separately from the axial diameters, as requested by the player.

| Hole | Bottom edge | Axial diameter | Centre | Pad OD | Cup OD |
|---|---:|---:|---:|---:|---:|
| 4 | 79.15 | 5.09 | 81.695 | 9.59 | 11.49 |
| 5 | 62.05 | 7.80 | 65.950 | 12.30 | 14.20 |
| 6 | 35.30 | 7.60 | 39.100 | 12.10 | 14.00 |

Centre spacings are 15.745 mm and 26.850 mm. Hole 3 is included as a reference
at centre 102.90 mm, diameter 5.80 mm. The unkeyed hole 3 bottom edge is 100 mm.

Transverse sizes of holes 5 and 6 are unconfirmed. The model uses circular
clearance envelopes with the measured axial diameters, conservatively covering
holes whose transverse dimensions do not exceed those values. These envelopes
are not a claim that the real holes are circular or an acoustic whistle model.
The new pads require a sealing trial; only the hole-4 TPU pad has been tried.

## Frame and clamps

End clamps sit at 28.100 and 92.695 mm from the foot, with a third clamp
between keys 5 and 6 at 52.475 mm. The raised bands are
4 mm wide and the bolt supports 6 mm wide. The upper band stops at 94.695 mm,
leaving 5.305 mm to hole 3's bottom edge. Actual finger comfort remains a trial.
A continuous low spine joins the three reinforced hinge pedestals. The pin
approach and key-tail clearance are retained. Each opening stop engages at 20°.

The new frame uses the revised 14.3 mm seats for bare 14.2 mm brass and a
1.2 mm split gap. It requires the matching caps supplied here. A CAD closure
check establishes seat contact before the clamp faces bottom out; it does not
establish actual gripping force. Fit without a liner and verify the printed
clamp holds. The previously requested cap-only fix for the old single-key frame
is not needed to assemble this longer three-key frame; the old single-key files
remain separate. Captive M2 nuts remain a lower-priority follow-up.

## Hardware and assembly

- Three steel pins, 1 mm diameter × 12 mm long.
- Three compression springs, nominal 2 mm OD × 5 mm free length, assumed 2 mm
  solid length and 0.3 mm wire. Spring rates are still unknown.
- Six M2 bolts and six external M2 nuts; check the existing bolt lengths fit.
- PETG frame, three caps and three keys; three 95A TPU pads and pad adhesive.

Each fixed bearing bore is 1.1 mm for the requested fit trial; each moving bore
is 1.25 mm. Each peg is 1.5 mm long, tapering from 1.2 to 1.0 mm diameter. The
nominal spring seat spacing remains 2.8 mm closed and about 3.70 mm open.

Install pins in order **4, then 5, then 6**. Feed from the foot end through
lower empty bearing bores. A straight 1 mm wire used as an assembly pusher can
advance the upper pin through the lower bearings; remove it after seating each
12 mm pin. Do not fit the lower pins first, because they block that route.
The CAD checks this entire insertion sequence including previously seated pins,
keys, frame, caps, tube and nominal M2 head envelopes. Physical manipulation
and spring fitting still need a trial on this longer assembly.

## Print files

Open the 3MF as a project in Bambu Studio, select the actual material and bed
profiles, then slice and inspect supports. These files contain no G-code.

- `exports/three-key/whistle-three-key-P1S.3mf`: PETG coupon plate, PETG mechanism
  plate, and a separate TPU plate containing all three pads.
- `exports/three-key/whistle-three-key-P1S-dry-fit-PETG.3mf`: all eleven pieces on
  one PETG plate, including rigid pads for a mechanical trial only.
- `exports/three-key/assembly-open.step`: complete assembly for review.
- `exports/three-key/print-oriented/`: separate STEP/STL parts; print the cap
  three times. Key and pad filenames identify the intended hole number.

The frame rests flat on its base. Keys rest on their finger faces, caps
on end faces, and pads on their flat backs. Supports are enabled for the frame
and keys. PETG uses 0.16 mm layers and four walls; TPU pads use 0.12 mm layers
and solid infill. Use ordinary 95A TPU from the external spool. Keep the parts
identified by hole number; pads 5 and 6 are similar in size but distinct.
The latest single-key hole-4 key/pad can be reused if already printed; older
versions should be compared with the supplied files.

## Verification

`tests/test_three_key.py` checks measured positions, valid solids and export
round trips, 21 positions for each key, actual stop contact and overtravel,
1 mm open-airway clearance, seal coverage, at least 1 mm key/pad clearance to
caps, and the mounting and pin-insertion checks described above. Key-to-key
clearance is checked from axial extents, which remain invariant under their
hinge rotation, covering independent key combinations. Frame collision checks
use exact frame sections spanning the full invariant axial extent of each key.

The shared 3MF tests verify quantities, mesh integrity, materials, plate layout,
and preserved orientation for both single-key and three-key projects. CI builds
and tests both prototypes. These checks do not replace physical trials of grip,
finger access, print strength, spring feel or sound.

Regenerate and package from the repository root:

```sh
python scripts/build_ci.py --model three_key --output build/three-key
python scripts/package_3mf.py --three-key --source build/three-key --output build/three-key/whistle-three-key-P1S.3mf
python scripts/package_3mf.py --three-key --source build/three-key --dry-run --output build/three-key/whistle-three-key-P1S-dry-fit-PETG.3mf
```

The assembly STEP contains solid cylindrical spring envelopes for illustration.
They deliberately overlap the locating pegs and sockets; they are not printable
parts or a model of the coil wire. The separate printable parts pass solid and
mesh validation.

## Opposite-side frame rail

A 5 mm wide rail joins the two clamp bases on the side opposite the keys,
closing the frame to resist twisting. Both lower rails are flush with the
clamp-base bottoms, giving a continuous flat printing base. The rail stays
below the tube and outside its surface, preserving the cap split and pin route.
Only the frame needs reprinting relative to the first three-key version.
Physical stiffness and thumb comfort remain trial checks.

## Middle clamp between keys 5 and 6

A third clamp at 52.475 mm is centred in the measured 19.15 mm edge gap
between holes 5 and 6. Its cap is identical to the end caps. Six M2 bolt
passages are drilled through the completed frame, including the raised spine.
The movement, mounting and insertion checks include all three clamps.
Compared with the first three-key prototype, reprint the frame and one extra
cap, and add two M2 bolts and nuts. Existing keys, pads and two caps are reusable.
Both 3MF projects now contain eleven pieces and orient the frame flat on its base.

The raised hinge-side spine steps down locally at the middle clamp, with 0.2 mm axial clearance at each side, so the cap can seat and tighten. Both lower rails remain continuous.
