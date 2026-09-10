# 35° opening and 1 mm EVA liner prototype

The three identical keys now open to 35° (previous released design: 20°). The
TPU parts are curved carriers for the user's 1 mm EVA foam sheet. The existing
2 mm OD × 5 mm compression springs, 1 × 12 mm pins and M2 hardware are retained.
The ordered 3 mm springs are not included in this revision.

## Opening and spring limits

At the nominal open stop, pad-centre lift is 4.670 mm and the shortest distance
from the uncompressed EVA surface to the whistle is 3.305 mm. The previous
20° TPU-only design had approximately 1.754 mm minimum clearance. All three
keys share this geometry.

The spring seats move from Z = 2.9 to 3.1 mm to clear the hinge collar throughout
travel. Closed spring length remains 2.8 mm; open length is 4.624 mm, leaving
0.376 mm nominal compression. The spring rate is unknown, so this does not
establish the actual return force. The assumed 2 mm solid length is unchanged.
At 40°, moving the seats high enough to retain hinge clearance would leave only
about 0.072 mm compression; 35° is the trial chosen to preserve some preload.

The frame stop and the clearance below the key tail are revised for the larger
opening. A 0.8 mm bevel on each spring holder’s upper rear corner clears the
flared carrier during travel. Print the new frame and keys together; reuse the clamp caps and hardware.
The TPU carriers are also new. The full assembly STEP includes EVA reference
solids, but these are not included as printed parts in the 3MF.

CAD clearance cannot establish whether the pads affect tone. Compare each open
note with the unkeyed whistle, then check rapid release and comfortable closing
travel. More opening also means more finger travel. The return force and sound
need a playing test before this becomes a settled design.

## Cutting and fitting the EVA

Print the cutting guide in PETG, with its flat base on the bed. It is included
on the PETG parts plate and supplied separately as `eva-cutting-template.3mf`.
The raised grip makes it easier to hold while tracing its outside edge.

1. Trace the guide onto the 1 mm EVA sheet and cut around the line. Make one
   liner first to check the fit, then repeat for the other two keys.
2. The outline is approximately 16.28 × 12.30 mm. Its long direction, parallel
   to the grip, goes **across** the whistle; its short direction runs along it.
3. Curve it onto the concave face of the new TPU carrier. It covers the whole
   face: do not cut a hole in its centre. Check the edge alignment before gluing.
4. Use a thin, even glue layer suitable for the actual EVA and TPU. Keep glue
   off the sealing surface. Seat the carrier tabs in the existing key-ring
   notches and glue the carrier into the ring.
5. Test one pad for leakage and reliable opening before fitting all three.

The guide is an unrolled outline at the sheet's mid-thickness radius, rather
than a flat projection of the curved pad. The TPU carrier flares slightly to
support the outside of the bent foam. Nominal closure assumes 0.2 mm EVA
compression; foam hardness and adhesive thickness are not measured, so this
is a prototype allowance, not a proven seal pressure.

## Printing and verification

Use the normal P1S 3MF for PETG frame/keys/guide and TPU 95A carriers. The PETG-only
package is a dry-fit option, not the intended flexible carrier. Existing support
settings for the frame and keys are retained. The guide prints flat without
supports. The carrier flare extends about 0.9 mm beyond its glue-body edge;
the automatic printability check flags this small lip and a local 0.68 mm wall.
Carrier supports remain disabled for this TPU trial: inspect the first print
for droop and complete walls before making all three. All three keys, carriers
and cut liners are interchangeable.

Automated checks cover 21 travel positions per key, stop engagement, spring
solid-length margin and at least 0.35 mm preload, 0.2 mm spring/hinge clearance,
open airway, at least 3 mm open pad clearance, seal coverage around each hole,
carrier fit, printable solids and the cutting-guide outline. These verify the
nominal CAD model, not printing tolerances, fatigue strength or acoustic results.
