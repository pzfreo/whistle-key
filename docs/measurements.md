# Whistle measurements

Instrument: brass Burke high-D whistle. All lengths are millimetres.
Hole numbers count from the mouthpiece. Positions are measured from the open
foot towards the mouthpiece. Bottom means footward; top means mouthpieceward.

## Measurement basis

The player requires independent positions measured from the physical whistle
foot to each hole's bottom edge. Do not chain the gaps to establish positions:
that accumulates measurement errors. Retain the rechecked gaps as cross-checks.
Absolute bottom-edge readings need reconciliation before updating the CAD.

| Hole | Previously measured bottom edge from foot | Next measurement |
|---|---:|---|
| 3 | 100.00 | Rechecked directly from foot; replaces 98.7 |
| 4 | 79.15 | Rechecked directly from foot; replaces dictated 79.23 |
| 5 | 62.05 | Rechecked directly from foot; replaces 60.87 |
| 6 | 35.30 | Rechecked directly from foot; replaces 34.1 |

Hole 4's earlier 81.68 mm reading was recorded as a centre, not a bottom edge.
The hole diameters and rechecked gaps below remain recorded observations.

| Measurement | Value | Status |
|---|---:|---|
| Tube outside diameter | 14.2 | Measured; cylindrical at clamp locations |
| Hole 3 axial diameter | 5.8 | Supplied diameter, treated as axial |
| Hole 4 axial diameter | 5.09 | Remeasured and confirmed |
| Hole 4 transverse diameter | 5.09 | Earlier measurement; circular model |
| Hole 5 axial diameter | 6.5 | Supplied diameter, treated as axial |
| Hole 6 axial diameter | 6.37 | Supplied diameter, treated as axial |
| Hole 6 bottom edge from foot | 34.1 | Measured reference, not rechecked in latest message |
| Hole 3 bottom to hole 4 top | 15.6 | Rechecked; replaces 15.7 |
| Hole 4 bottom to hole 5 top | 9.22 | Rechecked; replaces 9.2 |
| Hole 5 bottom to hole 6 top | 19.2 | Rechecked and confirmed |

## Gap-chain calculation: cross-check only, not adopted

| Hole | Bottom edge | Centre | Top edge |
|---|---:|---:|---:|
| 3 | 96.08 | 98.98 | 101.88 |
| 4 | 75.39 | 77.935 | 80.48 |
| 5 | 59.67 | 62.92 | 66.17 |
| 6 | 34.1 | 37.285 | 40.47 |

Calculation proceeds from the foot: hole 6 top = 34.1 + 6.37 = 40.47;
hole 5 bottom = 40.47 + 19.2 = 59.67; hole 4 bottom = 59.67 + 6.5 +
9.22 = 75.39; hole 3 bottom = 75.39 + 5.09 + 15.6 = 96.08.
Centres are bottom edge plus half the axial diameter.

| Centre spacing | Derived value |
|---|---:|
| Hole 3–4 | 21.045 |
| Hole 4–5 | 15.015 |
| Hole 5–6 | 25.635 |

Decimal precision reflects arithmetic, not additional measurement accuracy.
Chaining also accumulates diameter and gap errors, so this table is not the
source of truth for absolute positions.

## Unresolved discrepancies

The independent bottom-edge readings (hole 3 now rechecked at 100.00, plus
hole 5 at 60.87 and hole 6 at 34.1 awaiting recheck) and the earlier
hole 4 centre reading (81.68) conflict with the gap-chain calculation. Neither
set is silently substituted for the other. Await rechecked independent bottom
edges, then calculate each centre separately using its diameter. Hole 6's old
CAD diameter 5 and centre 43 were provisional. Earlier clearance claims must
be recalculated using the reconciled measurements.

## Prototype status and pending geometry

The current CAD source and exports have not yet been updated to the latest
measurements. The player prefers retaining the existing printed frame and
shortening replacement cap legs to recover tightening travel. That cap-only
revision is pending; the recent full-frame redesign is not the intended replacement.
The existing printed frame uses clamp offsets of +13 and -9 from hole 4.

No liner was installed. The clamp faces met without gripping adequately.
The spring and hinge were successfully assembled and operated; the TPU pad
made a reasonable seal. Finger interference and key catching remain P1 issues.
Captive M2 nuts are a lower-priority request.

The current pin-fit trial is 1.1 mm fixed bores for a 1.0 × 12 mm steel pin;
the moving bore remains 1.25 mm. The pad diameter remains 9.59 mm, based on
hole 4's confirmed 5.09 mm diameter, with a continuous concave contact face.
Tube wall/bore and circumferential hole alignment remain provisional.

Hole 3 bottom edge rechecked independently from the foot: 100.00 mm. With the recorded axial diameter of 5.8 mm, its centre is 102.90 mm and top edge 105.80 mm. This supersedes the earlier 98.7 mm bottom-edge reading; the gap-chain table above remains a non-adopted cross-check only.

Latest independent readings: hole 4 bottom edge 79.15 mm (dictation corrected from 79.23), hole 5 bottom edge 62.05 mm. Derived separately from the recorded diameters: hole 4 centre 81.695 mm and top 84.24 mm; hole 5 centre 65.30 mm and top 68.55 mm. Hole 6 bottom edge 34.1 mm remains awaiting independent recheck.

## Completed independent edge measurements — current reference

All four bottom edges have now been independently rechecked from the foot.
This table supersedes the historical calculations and pending-recheck notes above.

| Hole | Bottom edge | Axial diameter | Derived centre | Derived top edge |
|---|---:|---:|---:|---:|
| 3 | 100.00 | 5.80 | 102.90 | 105.80 |
| 4 | 79.15 | 5.09 | 81.695 | 84.24 |
| 5 | 62.05 | 6.50 | 65.30 | 68.55 |
| 6 | 35.30 | 6.37 | 38.485 | 41.67 |

Hole 6 bottom edge 35.30 replaces 34.10. Independent positions are the source
of truth; direct gaps are cross-checks only. Derived edge gaps are 15.76 mm
(3–4), 10.60 mm (4–5), and 20.38 mm (5–6), compared with direct gap readings
15.6, 9.22, and 19.2. These discrepancies are retained rather than averaging
or shifting the independent positions. CAD updates remain pending.
