# Burke whistle key attachment — design brief

Status: single-key development prototype, not yet fitted or played.
Updated: 6 September 2026.
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
- Prototype a custom 95A TPU pad with a curved sealing lip.
- Print rigid parts in PETG on a Bambu Lab P1S; print the TPU separately.
- Keep dimensions in millimetres and geometry parametric in build123d.

## Mechanical layout

Two split clamps, immediately above and below hole 4, carry a short side rail.
The rail carries two pivot supports, spring seat and fixed movement stops.
A lever pivots about an axis parallel to the whistle and reaches sideways over
the hole. Its round upper contact accepts the finger; the pad beneath closes
against the outside of the brass tube.

The spring pushes the lever open against a fixed stop. Some compression remains
at the open position to provide positive return. Deliberate finger pressure
closes the key against the spring. The closing stop limits pad compression and
takes additional finger load. Spring force at the finger depends on the lever
geometry as well as the unknown spring rate.

The prototype retains two clamps for mounting stability. Check that their
position leaves room for the other fingers and does not obstruct adjacent holes.
The CAD reference tube is only a lower tube segment, not a complete acoustic
model of a whistle.

## Pad and seal

The current trial pad is a separate TPU insert with a flat backing and a concave
cylindrical face matching the nominal outside of the tube. A central relief
leaves a continuous sealing lip surrounding the hole. A continuous roof closes
the opening; this is not an open ring or a plug pushed into the tone hole.

A rectangular boss on the rigid key fits a recess in the pad backing. It locates
the pad and prevents it rotating out of alignment with the tube. The fit has
clearance and is not a snap fastening: retention still requires selection and
trial of a removable adhesive suitable for the actual PETG and TPU.

The lip is intended to obtain compliance from its geometry despite 95A TPU's
relative firmness. Printed texture, seams and inaccurate alignment may cause
leaks. The current dimensions are experimental; CAD validity does not prove
airtightness. Retain the option of a soft silicone sealing layer if printed TPU
cannot seal reliably at a comfortable force.

## Dimensions and assumptions

Instrument measurements are unavailable. The player authorised provisional
high-D dimensions, to be replaced when the actual whistle can be measured.

| Item | Current value | Basis/status |
|---|---:|---|
| Tube outside diameter | 12.7 mm | Provisional; not a Burke measurement |
| Tube wall | 0.396875 mm | Provisional; bore derived from OD and wall |
| Hole 4 centre from open foot | 85 mm | Provisional |
| Hole 5 / 6 centres from foot | 68 / 43 mm | Reference only; provisional |
| Hole 4 / 5 / 6 diameters | 6 / 6 / 5 mm | Provisional |
| Single-key frame length | 32 mm | Derived from current clamp layout |
| Clamp width, each | 6 mm | Prototype choice |
| Nominal split gap | 0.8 mm | Must retain tightening travel when fitted |
| Liner allowance, radial | 0.5 mm | Liner material/compression unselected |
| Finger contact diameter | 11 mm | Prototype choice |
| Pad-centre opening movement | 6 mm | Increased to clear the curved lip; acoustic/comfort trial required |
| Pivot pin | 1 × 12 mm | User-identified steel dowel |
| Support / moving-key bore | 1.0 / 1.25 mm | Tune printed fit using coupon |
| M2 screw clearance | 2.4 mm | Prototype choice |
| TPU pad outside / relief diameter | 10.5 / 8.5 mm | Experimental |
| TPU lip relief height | 0.8 mm | Experimental |
| Nominal pad/tube radial interference closed | 0.2 mm | Intended elastic compression, not rigid clearance |
| Pad locator boss | 3 × 2 × 0.8 mm | Rectangular; 0.2 mm total lateral clearance |
| Compression spring OD / free length | 2 / 5 mm | User-found spring; treated as OD and free length |
| Spring solid length | 2 mm | Explicit user assumption, not supplier data |
| Spring rate | Unknown | Establish suitability by physical trial |
| Closed / open spring seat spacing | About 2.80 / 4.64 mm | Calculated from current geometry |

The spring has about 0.80 mm clearance above its assumed solid length at closure.
Its actual safe working stroke and force are unverified. The model shows a
cylindrical spring envelope, not a simulated coil; check retention and rubbing
as the upper seat tilts.

The clamp split gap alone does not guarantee gripping force. The liner and
actual bore fit must allow the halves to compress the liner and hold the whistle
before the split faces meet. Tighten evenly and check both slipping and marking.

## Prototype bill of materials

| Component | Quantity | Material or specification |
|---|---:|---|
| Frame | 1 | PETG |
| Lever | 1 | PETG |
| Identical lower clamp caps | 2 | PETG |
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

- The hinge barrel is flattened flush with the finger face, giving the key a
  broad flat printing surface.
- The pad has a recessed locator instead of a protruding peg, allowing its
  flat backing to lie on the bed with the sealing lip upwards.
- Sloping gussets support the spring seat and closing-stop shelf.
- Independent STEP/STL copies are oriented and placed at bed height.
- A small coupon tests horizontal 0.9, 1.0, 1.1 and 1.25 mm bores. With its
  clipped base corner at lower left when viewed from above, sizes increase from
  left to right. Use the same PETG/profile as the frame and trial the actual pin.

| Part | Recommended orientation |
|---|---|
| Frame | Split faces down; pivot supports up |
| Lower clamp caps | Flat semicircular end down; tube axis vertical |
| Lever | Flat finger face down; pad locator up |
| TPU pad | Flat backing down; curved sealing lip up |
| Fit coupon | Flat base down, as exported |

For a presumed 0.4 mm nozzle, initial settings discussed were 0.16 mm layers and
four walls for PETG, and 0.12 mm layers with solid construction for TPU. These
are untested starting points, not a calibrated printer profile. Inspect the
slicer preview, especially the 1 mm bores, small frame features and TPU lip.
Do not put support contacts on the sealing lip. Keep the TPU dry and follow its
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
thin regions, and a thin region in the TPU lip. It also flags possible tip-over
for the lever and clamp cap despite their broad planar bed faces; these warnings
have not been cleared by a slicer or physical print. Review adhesion and use a
brim if needed. This is not a fully validated production design.

The assembly STEP is a multi-body study, not a single printable object. The
spring envelope can intersect its seats slightly. Soft-pad interference in the
closed position represents intended compression, not a simulated deformation.

Before a playing trial:

1. Measure tube OD at both clamps and the hole; measure hole size, axial position
   and any offset around the tube. Confirm available finger and clamp space.
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
