# Burke whistle key attachment — design brief

Status: single-key development prototype, not yet fitted or played.
Updated: 7 September 2026.
Active parametric model: [`scripts/single_key.py`](../scripts/single_key.py).

## Purpose and player needs

Develop a removable key attachment for an existing brass Burke high-D tin
whistle. The player has Parkinson's disease and finds deliberate movements
against resistance easier to control than very light movements. The right index
finger, and to some extent the middle finger, can rest too close to a tone hole
and muffle notes even when that hole should be open.

The attachment should hold each affected hole positively open until the player
intentionally presses its key. The player should be able to rest a finger on the
contact without inadvertently shading the hole or partly closing the pad.
Required resistance and comfortable travel will be established by playing
trials, separately for each finger. Improvement in control is a design objective,
not a demonstrated result.

## Scope and agreed decisions

The eventual attachment covers holes 4, 5 and 6, numbered from the mouthpiece,
using three independent, normally open keys. The immediate prototype covers
only hole 4, operated by the right index finger. Validate this key before
extending the design to all three.

- Retain the existing instrument; use removable, lined split clamps.
- Use a printed supporting frame and a separate hinged finger lever.
- Use compression coil springs with fixed seats. Change resistance by replacing
  the spring, not by adding spring adjustment screws or torsion springs.
- Use a purchased 1 mm diameter × 12 mm steel dowel as the pivot. Hold it by
  friction in the fixed supports; provide running clearance in the moving key.
- Use the player's available M2 bolts and nuts for the clamp halves.
- Prototype a custom 95A TPU pad with a continuous curved sealing face.
- Print rigid parts in PETG on a Bambu Lab P1S; print the TPU separately.
- Keep dimensions in millimetres and geometry parametric in build123d.

## Mechanical layout

Two split clamps, immediately above and below hole 4, carry a short side rail.
The rail carries two pivot supports, spring seat and a fixed opening stop.
A curved lever wraps around the tube from a low side hinge, whose axis runs
parallel to the whistle at tube-centre height. Its round upper contact accepts the finger; the pad beneath closes
against the outside of the brass tube.

The spring pushes the lever open against a fixed stop. Some compression remains
at the open position to provide positive return. Deliberate finger pressure
closes the key against the spring. The TPU pad against the brass sets the closed
position; there is no separate rigid closing stop. Spring force at the finger depends on the lever
geometry as well as the unknown spring rate.

The prototype retains two clamps for mounting stability. Check that their
position leaves room for the other fingers and does not obstruct adjacent holes.
The CAD reference tube is only a lower tube segment, not a complete acoustic
model of a whistle.

## Pad and seal

The current trial pad is a separate TPU insert with a flat backing and a concave
cylindrical face matching the nominal outside of the tube, with 0.2 mm radial
interference for trial compression. The contact face is continuous across the
centre: the earlier annular lip and central relief have been removed at the
player’s request. The opposite backing is plain and flat.

A shallow retaining ring on the rigid key forms a flat-bottomed pad cup. Glue
the pad into this ring, aligning its curved face with the whistle before the
glue sets. The ring is 1.2 mm deep, with 0.8 mm walls and 0.3 mm total diametral
clearance around the pad. The TPU projects beyond the rigid rim so it contacts
the brass first. There is no central peg or recess in the pad backing.

The player will trial available 95A TPU first. Its firmness, printed texture,
seams and inaccurate alignment may cause leaks. The current dimensions are experimental; CAD validity does not prove
airtightness. Retain the option of a soft silicone sealing layer if printed TPU
cannot seal reliably at a comfortable force.

## Dimensions and assumptions

The player has supplied the [tube and hole 4 measurements](measurements.md).
Remaining unmeasured reference dimensions retain provisional high-D values.

| Item | Current value | Basis/status |
|---|---:|---|
| Tube outside diameter | 14.2 mm | Measured; cylindrical tube confirmed |
| Tube wall | 0.396875 mm | Provisional; bore derived from OD and wall |
| Hole 4 centre from open foot | 81.68 mm | Measured |
| Hole 5 / 6 centres from foot | 65.68 / 43 mm | Hole 5 derived from measured 16 mm spacing; hole 6 provisional |
| Hole 4 / 5 / 6 diameters | 5.09 / 6 / 5 mm | Hole 4 measured circular; holes 5/6 provisional |
| Single-key frame length | 28 mm | Lower clamp moved to clear hole 5 |
| Clamp width, each | 6 mm | Prototype choice |
| Nominal split gap | 0.8 mm | Must retain tightening travel when fitted |
| Liner allowance, radial | 0.5 mm | Liner material/compression unselected |
| Finger contact diameter | 11.49 mm | Widened to support retaining-ring wall |
| Pad-centre opening movement | 3.25 mm at 20° | Curved arm moves pad sideways as well as upwards; acoustic/comfort trial required |
| Pivot pin | 1 × 12 mm | User-identified steel dowel |
| Support / moving-key bore | 1.0 / 1.25 mm | Tune printed fit using coupon |
| M2 screw clearance | 2.4 mm | Prototype choice |
| TPU pad outside diameter | 9.59 mm | Derived from measured hole plus trial sealing margins |
| Nominal pad/tube radial interference closed | 0.2 mm | Intended elastic compression, not rigid clearance |
| Pad retaining ring | 9.89 mm ID, 11.49 mm OD, 1.2 mm deep | 0.3 mm diametral pad clearance |
| Compression spring OD / free length | 2 / 5 mm | User-found spring; treated as OD and free length |
| Spring solid length | 2 mm | Explicit user assumption, not supplier data |
| Spring rate | Unknown | Establish suitability by physical trial |
| Closed / open spring seat spacing | About 2.80 / 3.70 mm | Calculated from current geometry |

The spring has about 0.80 mm clearance above its assumed solid length at the
nominal modelled closure. Actual pad compression depends on finger force; this
is not a hard limit enforced by a rigid stop.
Its actual safe working stroke and force are unverified. The model shows a
cylindrical spring envelope, not a simulated coil; check retention and rubbing
as the moving seat tilts.

The spring is located in a 2.4 mm diameter fixed sideways socket, initially 1.5 mm deep,
and by a peg on the curved arm, 1.5 mm long with a 1.2 mm base tapering to a 1.0 mm tip.
The user's 0.3 mm wire gives a nominal 1.4 mm spring bore. The raised socket wall
provides retention without reducing initial preload. Increasing
`spring_floor_extra_depth` deepens only the floor towards the tube and reduces compression;
currently it is zero. Open preload displacement is about 1.30 mm, so available
floor-depth adjustment is limited. Retention and rubbing still need a trial.
The old `spring-socket-section.png` shows the superseded upright layout; turn count was illustrative.

The clamp split gap alone does not guarantee gripping force. The liner and
actual bore fit must allow the halves to compress the liner and hold the whistle
before the split faces meet. Tighten evenly and check both slipping and marking.

## Prototype bill of materials

| Component | Quantity | Material or specification |
|---|---:|---|
| Frame | 1 | PETG |
| Lever | 1 | PETG |
| Identical upper clamp caps | 2 | PETG |
| Curved pad insert | 1 | 95A TPU |
| Pivot dowel | 1 | Steel, 1 × 12 mm |
| Return spring | 1 | Compression coil, nominal 2 × 5 mm |
| Clamp bolts | 4 | M2; 12 mm length proposed, confirm with actual nuts |
| Clamp nuts | 4 | M2 external nuts |
| Clamp lining | As needed | Soft, non-marking material; nominal 0.5 mm |
| Pad attachment | As needed | Removable adhesive, type to be selected |

The hinge-fit coupon is an optional PETG test print, not an installed component.

## Manufacture and assembly

Manufacturing changes included in the model:

- The hinge has short 3 mm thick cheeks with 6 mm wide roots, replacing the
  tall posts that broke in the first trial. The moving hub is 4 mm long.
- The pad has a plain flat backing for printing; the retaining ring prints
  upwards on the inverted key.
- A sideways spring housing keeps the spring below the playing surface.
- A broad angled opening stop meets the rear tail at 20°, verified by contact
  and overtravel tests. Physical strength and wear remain trial requirements.
- Independent STEP/STL copies are oriented and placed at bed height.
- A small coupon tests horizontal 0.9, 1.0, 1.1 and 1.25 mm bores. With its
  clipped base corner at lower left when viewed from above, sizes increase from
  left to right. Use the same PETG/profile as the frame and trial the actual pin.

| Part | Recommended orientation |
|---|---|
| Frame | Outer rail side down; supports enabled |
| Upper clamp caps | Flat semicircular end down; tube axis vertical |
| Lever | Flat finger face down; curved arm up; supports enabled |
| TPU pad | Flat backing down; curved contact face up |
| Fit coupon | Flat base down, as exported |

For a presumed 0.4 mm nozzle, initial settings discussed were 0.16 mm layers and
four walls for PETG, and 0.12 mm layers with solid construction for TPU. These
are untested starting points, not a calibrated printer profile. Inspect the
slicer preview, especially the 1 mm bores, small frame features and TPU contact face.
Do not put support contacts on the sealing face. Keep the TPU dry and follow its
manufacturer's settings; use external feeding for ordinary 95A TPU.

Use the coupon to choose friction grip without forcing the pin into a fragile
support. The moving lever must rotate freely. Select `pivot_support_clearance`
from the print result; do not assume a nominal 1 mm printed hole grips a 1 mm
rod correctly. The short coupon does not reproduce every aspect of the full
hinge; verify the assembled hinge too.

## Verification and acceptance

See [engineering assertions and usability acceptance tests](acceptance-tests.md)
for the requirements, automated checks and physical trial criteria.

CAD checks performed include valid, watertight individual part solids, 21-position
key and pad clearance checks through the opening motion,
and a frame-to-tube interference check after adding gussets.

Automated printability analysis no longer reports the frame's flat cantilever
shelves after the gussets were added. It still flags small frame features and
thin regions, and a thin region in the TPU contact face. It also flags possible tip-over
for the lever and clamp cap despite their broad planar bed faces; these warnings
have not been cleared by a slicer or physical print. Review adhesion and use a
brim if needed. This is not a fully validated production design.

The assembly STEP is a multi-body study, not a single printable object. The
spring envelope can intersect its seats slightly. Soft-pad interference in the
closed position represents intended compression, not a simulated deformation.

Before a playing trial:

1. Tube OD, hole 4 size/position and hole 4–5 spacing are recorded. Confirm
   adjacent-hole diameter, any offset around the tube, and finger/clamp space.
2. Print the fit coupon and verify pin grip and running clearance.
3. Inspect and assemble the rigid parts, liner, spring and pad; verify spring
   retention, free movement and clearance above solid at full closure.
4. Confirm a repeatable seal at comfortable finger pressure, including low notes.
5. Compare the open-hole sound with the attachment removed, including while
   resting a finger on the key. The pad must not audibly shade the open hole.
6. Check deliberate closing, reliable return, fatigue, finger contact comfort,
   and resistance to slipping or marking the brass during normal playing.
7. Repeat opening/closing and check for pin migration, loose pads, wear and leaks.

Revise from those results before extending to holes 5 and 6. No target finger
force, service life or quantitative acoustic tolerance has yet been agreed.

## Repository map and references

- [`scripts/single_key.py`](../scripts/single_key.py): active parameter block and
  reproducible geometry. Edit this for the current prototype.
- [`exports/single-key/`](../exports/single-key/): assembled STEP and individual
  parts in assembly coordinates.
- [`exports/single-key/print-oriented/`](../exports/single-key/print-oriented/):
  oriented individual STEP/STL files, including the pin-fit coupon.
- [`scripts/whistle_keys.py`](../scripts/whistle_keys.py): earlier three-key
  layout study. Its spring and pivot specifications are superseded for the
  active single-key prototype.
- [`parameters.json`](../parameters.json): legacy three-key parameter inventory,
  not an input to either model.

The [Humphrey high-D information](https://humphreywhistles.github.io/) informed
provisional tube sizing; it does not establish Burke dimensions. The
[Triple Play recorder account](https://www.jefftk.com/p/triple-play-recorder)
provides a related retrofit example and observations about sealing pressure.
[Flexo's compression-spring catalogue](https://www.flexosprings.com/stock-springs/compression-springs)
was investigated earlier; the current prototype instead follows the user's
2 × 5 mm spring assumptions. For material handling, see
[Bambu's TPU 95A guidance](https://uk.store.bambulab.com/collections/all/products/tpu-95a-hf),
while using the actual filament manufacturer's settings for printing and drying.

## First dry-fit feedback and curved-arm revision

The player confirmed the 1.0 mm printed bore fits the purchased pin. The first
frame's supports broke too easily, the opening stop did not work, and the tall
hinge obstructed the finger reaching the hole. Those are failed physical
requirements, not resolved by the earlier CAD collision tests.

This revision lowers the hinge beside the shaft and curves the arm up to the
pad, following the flageolet arrangement suggested by the player. The fixed
frame now carries the lower clamp halves; the removable caps are above. The
1 × 12 mm dowel, M2 fasteners and glued concave pad are retained. The spring
now acts sideways. Its rate and the resulting finger force are still unknown.
Repeat the PETG dry fit to assess finger access, cheek strength and the stop
before evaluating the TPU seal. See `curved-key-layout.png` for an end view
with the clamp rings omitted to expose the mechanism.

## Pin insertion access revision

The clamp joint now sits 7 mm below the pivot axis. Its tabs and the connecting
rail are lowered together; the rail top is 7.4 mm below the pivot. The upper
caps consequently extend farther down beside the tube. An open throat lets
them lift straight off rather than requiring sliding from the whistle end. Wider inward tab connections
join the clamp arcs without changing the M2 bolt centres or 0.8 mm split gap.
The existing key, 1 mm fixed bores and 1 × 12 mm pin are unchanged.

A continuous cylindrical sweep checks the entire 12 mm pin insertion from
beyond the lower clamp through the hinge. An additional 0.1 mm radial approach
allowance clears the frame, caps and tube; nominal 4 mm diameter × 2 mm tall
M2 head envelopes also clear. Actual head dimensions and hand access need a
dry fit. The lower rail lengthens the bearing supports; their 3 mm cheeks and
6 mm roots are retained, but printed strength must be checked again.

Print the updated frame and both caps together; the previous caps do not fit
the lowered joint. Insert the pin from the foot end, along the path illustrated
in `pin-insertion.png`. This revision checks pin access, not spring installation.

## Full-width hinge pillar reinforcement

Both pillars now broaden to the full 7.4 mm rail width from 1.2 mm below the
pivot axis down into the rail. These solid 3 mm thick buttresses replace the
tapered lower stems, adding about 91 mm³ of material to the frame. The pin
bores, insertion corridor, key and caps are unchanged. CAD verifies clearance
and solid continuity; improved printed strength still needs a physical trial.
Only the frame needs reprinting relative to the lowered-joint revision.

## Joined clamp base and enlarged spring peg

The notches where each lower clamp arc meets its rectangular tabs are filled
with a continuous base across the clamp width. The liner recess is retained.
This joins the arc and rectangular sections directly, as requested, without
changing the split gap, bolt holes or pin approach.

The spring peg is enlarged to 1.2 mm at its base, 1.0 mm at its tip and 1.5 mm
long. Against the assumed 1.4 mm spring bore this leaves 0.2 mm diametral
clearance, reduced from 0.4 mm. The larger peg needs a printed fit trial; spring
force settings are unchanged. Reprint the frame and key for this revision;
reuse the current caps and pad.

## Rounded key-arm shoulder

The sharp inside shoulder above the spring housing now has a 0.8 mm concave
fillet across the full 4 mm arm width. This adds material into the corner and
replaces the abrupt change of direction with a tangent radius. The CAD radius
is controlled by `arm_transition_radius`; the housing clearance and movement
checks still apply. This is a local stress-concentration improvement, not a
measured strength rating. Only the key needs reprinting for this revision.
See `key-arm-transition.png`.

The next friction-fit trial uses 1.1 mm fixed hinge bores with the existing 1.0 × 12 mm steel pin. The moving key bore remains 1.25 mm. This supersedes the 1.0 mm frame bore for the next print; retention is not yet confirmed. Only the frame changes.
