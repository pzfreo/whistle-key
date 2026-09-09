# Hinge support reinforcement — 9 September 2026

A fixed hinge support broke while the user inserted its steel pin. The exact fracture location has not yet been confirmed. This revision adds stock around the bore and along the stem, with a lead-in to reduce snagging during insertion.

| Feature | Previous | Revised |
|---|---:|---:|
| Rounded fixed bearing head diameter | 4 mm | 6 mm |
| Stem width above the broad pedestal | 4 mm | 6 mm |
| Bearing axial thickness | 3 mm | 3.2 mm |
| Radial material above working bore | 1.45 mm | 2.45 mm |
| Pin entry lead-in | None | 0.25 mm deep, 45° each end |
| Straight working bore | 1.1 mm | 1.1 mm |
| Pin | 1 × 12 mm | 1 × 12 mm |

The larger fixed heads are independent of the rotating key hub radius. The inner bearing faces retain the 0.3 mm axial clearance to the existing key. A fitted pin projects nominally 0.5 mm beyond each outer bearing face. The lead-ins leave 2.7 mm of straight bearing bore in each support and 2.2 mm minimum radial stock at the mouths. Existing keys, pads and clamp caps are retained.

The frame volume increased from 6313.3134 to 6548.2970 mm³. MCP solid validity and STEP export gates pass. The geometric regression checks cover the thicker crowns and continuous stems; these do not establish printed breaking strength. Existing tests also check key travel and pin insertion paths.

Printability analysis of both old and revised frames reports the same 17 warnings: overhangs, a small vertical feature and an unlocated thin-wall warning. There are no reported errors, but this is not a support-free frame certification. The existing print package enables frame supports and uses 0.16 mm layers and four walls. Clamp-cap orientation is unchanged.

Physical pin fitting remains to be tested. Support the bearing locally when fitting the pin; if it binds, do not force it through. Printed bore fit and layer adhesion can still affect breakage despite the extra CAD material.

Validation completed: all 17 existing three-key tests passed, the new bearing-stock regression passed separately, and all four print-package tests passed. This includes the full 21-position travel sweep for each key, pin insertion order and clearance, clamp tightening, sealing envelopes, interchangeability, and exported mesh/STEP checks.
