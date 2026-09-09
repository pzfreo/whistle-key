# Measured three-key prototype

The working hole-4 mechanism is extended to holes 4, 5 and 6 on one 71.595 mm
frame. Each curved key has its own normally open coil spring, 1 × 12 mm steel
pin and glued concave TPU pad. All three keys and pads are now identical,
sized for the largest measured hole (7.80 mm). All geometry is metric and controlled
by `scripts/three_key.py`.

## Measurements and pad sizes

Bottom edges are independently measured from the whistle foot; centres are
derived separately from the axial diameters, as requested by the player.

| Hole | Bottom edge | Axial diameter | Centre | Pad OD | Cup OD |
|---|---:|---:|---:|---:|---:|
| 4 | 79.15 | 5.09 | 81.695 | 12.30 | 14.20 |
| 5 | 62.05 | 7.80 | 65.950 | 12.30 | 14.20 |
| 6 | 35.30 | 7.60 | 39.100 | 12.30 | 14.20 |

Centre spacings are 15.745 mm and 26.850 mm. Hole 3 is included as a reference
at centre 102.90 mm, diameter 5.80 mm. The unkeyed hole 3 bottom edge is 100 mm.

Transverse sizes of holes 5 and 6 are unconfirmed. The model uses circular
clearance envelopes with the measured axial diameters, conservatively covering
holes whose transverse dimensions do not exceed those values. These envelopes
are not a claim that the real holes are circular or an acoustic whistle model.
The player confirmed the recorded hole measurements on 2026-09-09. The common
pads require a sealing trial; only the earlier, smaller hole-4 TPU pad has been tried.

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
remain separate. Underside hex pockets now stop the M2 nuts turning.

## Hardware and assembly

- Three steel pins, 1 mm diameter × 12 mm long.
- Three compression springs, nominal 2 mm OD × 5 mm free length, assumed 2 mm
  solid length and 0.3 mm wire. Spring rates are still unknown.
- Six M2 bolts and six M2 nuts seated in underside hex pockets; check the existing bolt lengths fit.
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
  three times. Numbered key/pad filenames are retained for compatibility;
  their geometry is identical and each fits any of the three positions.

The frame rests flat on its base. Keys rest on their finger faces, caps
on end faces, and pads on their flat backs. Supports are enabled for the frame
and keys. PETG uses 0.16 mm layers and four walls; TPU pads use 0.12 mm layers
and solid infill. Use ordinary 95A TPU from the external spool. Print three
identical keys and three identical pads; no markings or sorting are needed.
The frame, caps, pins and springs are reusable. The previous hole-5 key/pad
already has the common dimensions; the old hole-4 and hole-6 parts differ.

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

## Underside M2 nut pockets

All six bolt positions have hexagonal pockets opening from the bottom of the
frame. Each pocket is 4.30 mm across flats and 1.90 mm deep. The default nut
is 4.00 mm across flats and 1.60 mm thick, matching this
[Accu M2 DIN 934 specification](https://www.accu.co.uk/hexagon-nuts/766417-NUT202M2).
Actual nut dimensions have not yet been confirmed by the player. Dimensions
and print clearance are parameters near the top of `scripts/three_key.py`.

Local 7 mm diameter bosses leave at least 1 mm material outside pocket corners
and a 1.6 mm bearing roof above each nut. Bolt centres and clamp interfaces are
unchanged. The frame stays flat on the bed; inspect and remove any support
inside the pockets before inserting nuts. Only the frame needs reprinting.

Insert nuts from underneath, flat against the pocket roofs, then engage the
bolts from above. The hex walls prevent rotation once engaged. These are open
pockets, not snap-fit retainers: a small piece of tape can hold a nut while
starting its bolt. Bolts can protrude farther below the frame with recessed nuts.

Tests check the full nut insertion sweep, fit at the seated position, contact
with the bearing roof, blocked rotation and material around each pocket.
Printed nut fit and resistance to tightening torque still need a physical trial.
The nut-pocket revision retained individual pad sizes. On 2026-09-09 the player
confirmed the measurements and requested identical parts for all three positions.
The shared pad is 12.30 mm OD; cup ID is 12.60 mm and head OD is 14.20 mm.
Minimum axial head-to-head clearance is 1.545 mm throughout rotation. The
common geometry is tested for interchangeability, travel and sealing coverage.
The larger hole-4 head still needs a playing trial for finger comfort.


## Pad locating tabs — 2026-09-09

![Pad tabs and retaining-ring notches](pad-locating-tabs.png)

All three common keys now have two opposed notches in the retaining ring,
aligned along the whistle axis. Each TPU pad has matching tabs, 1.6 mm wide,
0.9 mm thick and extending 0.75 mm beyond its 12.30 mm circular body. Overall
pad length across tabs is 13.80 mm, within the 14.20 mm key-head envelope.
Notches are 2.0 mm wide, giving 0.20 mm nominal clearance on each side.

The notches open from the pad side through the ring's 1.2 mm height. The tabs
are flush with the flat glue backing; the solid cup roof remains the seating
stop. Align the tabs with the notches and press the backing fully against the
roof before gluing. A 180-degree reversal is equivalent; a 90-degree rotation
is blocked. These are locating features, not snap-fit retainers.

The tabs sit above the tube crown and do not interrupt the curved sealing
face. Printing orientation stays the same: keys finger-face down, pads flat
back down. Print the new keys and pads together; reuse the frame and hardware.
Tests cover tab insertion, correct/incorrect orientation, full seating,
interchangeability, key travel and the continuous sealing band. Confirm the
nominal tab clearance in the PETG/95A TPU printing trial.
