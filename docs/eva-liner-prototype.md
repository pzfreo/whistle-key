# 35° opening and 2 mm EVA liner prototype

The three identical keys open to 35°. The 2 mm EVA foam sheet is now glued
directly to the key: there is no separate TPU carrier, no retaining ring and no
locating tabs. The pad face is part of the printed PETG key. The existing
2 mm OD × 5 mm compression springs, 1 × 12 mm pins and M2 hardware are retained.

![Closed pad section at hole 5](eva-2mm-pad-section.png)

## Integral pad face

Each key carries a dished boss on its underside. The dish is a cylinder of
8.9 mm radius, concentric with the whistle when the key is closed, which is
the 7.1 mm tube radius less 0.2 mm closure interference plus the 2 mm sheet.
The EVA fills that dish and seals against the brass.

- The glue surface is one continuous cylindrical face, 175.69 mm², with no
  ring, notch, step or parting line anywhere on it.
- 3.8 mm of solid PETG sits above the dish, so the key is its own pad backing.
  The earlier arrangement left a 0.8 mm TPU shell doing that job.
- The pad face is 14.2 mm across, the same envelope as the old retaining ring,
  leaving 1.545 mm between adjacent pads.
- Key volume rises from 749 mm³ to 957 mm³. The printed part count drops from
  ten files to five, since the three identical keys now export once as
  `lever_print`, and the TPU spool is no longer needed.

Because the whole 14.2 mm face is available for foam, the sealing footprint is
wider than the old 12.3 mm carrier gave, despite the thicker sheet. The
continuous band of foam around each hole at the nominal mid-compression
surface is 3.04 mm at hole 4, 1.68 mm at hole 5 and 1.78 mm at hole 6. The
previous 1 mm liner in a TPU carrier gave 2.29, 1.55 and 1.65 mm.

## Opening and spring limits

At the nominal open stop, pad-centre lift is 4.670 mm, the uncompressed EVA
surface clears the whistle by 4.042 mm and the key itself clears it by
2.270 mm. Closed spring length remains 2.8 mm; open length is 4.624 mm,
leaving 0.376 mm nominal compression against a 5 mm free length. The spring
rate is unknown, so this does not establish the actual return force.

CAD clearance cannot establish whether the pads affect tone. Compare each open
note with the unkeyed whistle, then check rapid release and comfortable closing
travel. The return force and sound need a playing test before this becomes a
settled design.

## Cutting and fitting the EVA

Print the cutting guide in PETG, with its flat base on the bed. It is included
on the PETG parts plate and supplied separately as `eva-cutting-template.3mf`.
The raised grip makes it easier to hold while tracing its outside edge.

1. Trace the guide onto the 2 mm EVA sheet and cut around the line. Make one
   liner first to check the fit, then repeat for the other two keys.
2. The outline is approximately 14.59 × 14.20 mm. Its long direction, parallel
   to the grip, goes **across** the whistle; its short direction runs along it.
3. Curve it into the dished face on the underside of the key. It covers the
   whole face: do not cut a hole in its centre. Check the edge alignment
   before gluing.
4. Use a thin, even glue layer suitable for the actual EVA and PETG. Keep glue
   off the sealing surface.
5. Test one pad for leakage and reliable opening before fitting all three.

The guide is an unrolled outline at the sheet's mid-thickness radius rather
than a flat projection of the curved pad, so it is wider across the whistle
than the 14.2 mm pad face. Nominal closure assumes 0.2 mm EVA compression;
foam hardness and adhesive thickness are not measured, so this is a prototype
allowance, not a proven seal pressure.

## Printing and verification

Every printed part is now PETG: frame, three keys, three clamp caps, cutting
guide and pin coupon. `whistle-three-key-P1S.3mf` puts all nine on a single
plate. Existing support settings for the frame and keys are retained. The
guide prints flat without supports.

Automated checks cover 21 travel positions per key, stop engagement, spring
solid-length margin and at least 0.35 mm preload, 0.2 mm spring/hinge
clearance, open airway, at least 3 mm open pad clearance, a 1.5 mm seal band
around each hole, a single uninterrupted glue face, printable solids and the
cutting-guide outline. These verify the nominal CAD model, not printing
tolerances, fatigue strength or acoustic results.
