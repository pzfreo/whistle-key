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

## Spring holder joined to the bearings

Following the user's marked screenshot, each spring upright now has a solid web on its whistle-facing side spanning into both bearing pillars. The web is 1.5 mm thick in X, spans 6.2 mm along the whistle and overlaps each pillar by 0.8 mm axially. It rises from the pedestal to the top of the spring holder; the rounded bearing profiles determine the upper extent of contact with the pillars. The spring socket is cut after the union so it retains its original open approach and depth.

Frame volume is now 6636.1026 mm³. MCP solid validity and STEP export gates pass. A focused regression verifies continuous stock across both former gaps and a clear spring insertion envelope. Printability analysis still reports 17 warnings and no errors; the three existing 0.3 mm overhang ledges have larger areas because of the webs. Existing frame support settings are retained. Printed strength remains to be confirmed by a physical trial.

All 18 existing three-key checks passed after this change, including each key's 21-position motion sweep and pin insertion. The new web/spring-access regression passed separately; all four print-package checks passed.

## Remove the two spring-holder overhangs

The user identified the rear lip and the flat shelf below the spring socket as unnecessary support generators. The back of each holder and its connecting web is now flush with the frame rail at X = −7.7 mm, removing the former 0.3 mm projection. This leaves 0.6 mm of material behind the unchanged blind socket floor at X = −8.3 mm. The webs still overlap both bearing pillars.

The second flat shelf, beneath the socket mouth, is replaced by a 50° sloping brace. It adds material beneath the mouth while retaining the original socket diameter and depth. The key-motion tests check the added brace against the rotating key.

Frame volume is 6573.7761 mm³. MCP validity and STEP export gates pass. Printability warnings decrease from 17 to 11: the three rear-lip and three socket-shelf overhang findings disappear. Remaining findings concern the nut-pocket roofs, spring bores, a small feature and an unlocated thin wall. The frame is not certified support-free; existing slicing settings are retained. A physical trial is still needed to confirm strength and printed spring fit.

Validation: all 19 existing three-key tests passed, including complete travel and pin/spring-access checks. The new flush-back/brace regression passed separately, and all four print-package tests passed.
