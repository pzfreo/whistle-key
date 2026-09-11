# Burke whistle assistive key specification

This document is the restart specification for the three-key prototype. It
records the measured instrument, the agreed mechanical interfaces, and the
current experimental choices. It is intended to be sufficient to rebuild the
design in a new CAD session. All dimensions are millimetres unless stated
otherwise. The parametric implementation is `scripts/three_key.py`.

## Purpose and scope

The attachment adds normally-open keys to holes 4, 5 and 6 of a cylindrical
brass Burke high-D tin whistle. The keys let the player close a hole with a
deliberate press while reducing accidental muffling from a resting right-hand
index or middle finger. The key must return positively to an open stop when the
finger is released.

This is an assistive prototype, not a finished musical-instrument mechanism.
Tone, intonation, airtightness, fatigue life, spring force and comfort require
physical trials. CAD clearances are nominal and do not account for printer
tolerance, glue, foam hardness or spring-rate variation.

## Instrument datum and measured holes

Use the open foot of the whistle as axial datum zero. The whistle is cylindrical
at the attachment and has 14.2 OD. Hole positions are measured independently
from the foot; do not reconstruct them by adding adjacent gaps.

| Hole | Bottom edge | Axial diameter | Derived centre | Derived top edge |
|---|---:|---:|---:|---:|
| 3 (reference) | 100.00 | 5.80 | 102.90 | 105.80 |
| 4 | 79.15 | 5.09 | 81.695 | 84.24 |
| 5 | 62.05 | 7.80 | 65.950 | 69.85 |
| 6 | 35.30 | 7.60 | 39.100 | 42.90 |

The hole 4 transverse reading is 5.09. Transverse dimensions of holes 5 and 6
are not confirmed. Until they are measured, the model uses circular envelopes
from the axial readings as conservative clearance references, not as an
acoustic model. The direct gap checks were: hole 3 bottom to hole 4 top 15.60,
hole 4 bottom to hole 5 top 9.22, hole 5 bottom to hole 6 top 19.20, and hole 4
bottom to hole 6 top 36.30.

## Key layout

There are three identical interchangeable keys. They are intentionally sized
for the largest measured hole and are not engraved or position-specific.

- Common pad/contact diameter: 12.30.
- Key pad face outside diameter: 14.20 nominal, matching the whistle OD
  envelope. Minimum axial clearance between adjacent pads is 1.545.
- The pad face is integral with the key: a dished boss on the key underside,
  cut by a cylinder of 8.90 radius concentric with the whistle at closure
  (7.10 tube radius, less 0.20 interference, plus the 2.0 sheet).
- The glue surface is one continuous cylindrical face of 175.69, with no
  retaining ring, tab notch, step or parting line on it.
- Solid PETG above the dish: 3.80.
- The separate TPU carrier, its retaining ring and the pad locating tabs are
  superseded, as is the earlier widened carrier flare.

The key is a curved arm around the whistle, with a 4.0-wide hinge region, 3.0
thickness, 3.5 rear tail extension, and a widened 6.0 upper load path. The
upper arm has 1.0 extra radial stock and a 0.8 transition radius. A continuous
rear/tangent web fills the former weak notch. The hinge pivot axis is parallel
to the whistle axis, at X = -11.2 and Z = 0 in the local section coordinates;
the derived arm radius is 11.2. The pivot pin is 1.0 diameter.

The nominal open angle is 35°. Rotation is toward the open stop. At that stop,
the calculated pad-centre lift is 4.670 and the current uncompressed EVA
surface is about 4.163 from the reference tube. The angle was increased from
the earlier 20°/30° trials to keep the pad away from the airway. Forty degrees
was rejected for the current spring geometry because it leaves almost no
compression reserve.

## Pad and seal

The current pad system has one part: a single piece of 2.0-thick EVA sheet
glued into the dished face of the key. There is no separate carrier and no
second EVA layer. The nominal model uses 0.20 compression allowance at closure;
this is a trial assumption, not a measured foam property.
The EVA cutting guide is approximately 14.59 × 14.20 and is unrolled at the
mid-thickness radius. Trace and cut one liner first, curve it into the key's
dished face, check the edge, then glue it with a thin even layer suitable for
the actual PETG
and EVA. Do not cut a central hole in the liner.

The pad is intended to seal around each hole while leaving the hole itself
open when the key is raised. The CAD sealing-band check probes the current
face around each hole; physical leak and tone tests are mandatory. The open
pad must not intrude into the immediate airway. A changed pad outline or liner
thickness requires rerunning the sealing, airway and travel tests.

## Hinge, pin and spring

Each key has one friction-held steel dowel and one sideways compression spring.

- Pin: 1.0 × 12.0 steel dowel.
- Fixed bearing bores: 1.10 nominal diameter, with 0.25 lead-in allowance.
- Moving key bore: 1.25 nominal diameter.
- Fixed bearing crown radius: 3.0; minimum continuous collar wall: 0.90.
- Bearing ears are 3.2 axial thickness, leaving about 0.5 pin projection at
  each end. Pin insertion is from the foot end, in order 4, then 5, then 6.
- Spring: nominal 2.0 OD × 5.0 free length compression coil. Solid height is
  assumed 2.0; wire is nominally 0.3. The spring rate is unknown and must not
  be inferred from these dimensions.
- Closed spring seat spacing: 2.80. Current open spacing: about 4.624, leaving
  about 0.376 nominal compression at 35°.
- Spring socket diameter: 2.4, socket depth 1.5. Moving peg is 1.2 at its
  base, tapering to 1.0 at a 1.5-long tip.
- Spring seats are at Z = 3.1 in the current design. An 0.8 bevel at the upper
  rear holder corner clears the key's pad boss during travel.

The ordered 3.0 × 5.0 springs are not part of this revision. If a spring is
changed, check both solid-height margin and positive return before changing
the opening angle.

## Frame, clamps and fasteners

The frame is a PETG printed structure with three split clamps, three reinforced
hinge pedestals, a continuous low spine and an opposite-side 5.0-wide return
rail. Clamp centres are 28.10, 52.475 and 92.695 from the foot. The middle
clamp sits between holes 5 and 6. End clamp bands are 4.0 wide; bolt supports
are 6.0 wide. The nominal clamp inner radius is 7.15 (14.3 diameter seat for
the bare 14.2 whistle), with 0.05 radial clearance and a 1.2 split gap.

Use the matching printed caps. The frame and caps have underside hex pockets:
4.30 across flats, 1.90 deep, for nominal M2 nuts 4.00 across flats × 1.60
thick. Pocket clearance and actual nut dimensions need a physical fit check.
M2 bolt head envelope is 2.4 diameter × 2.0 high. The user's M2 bolts and nuts
are the intended hardware; exact bolt length remains to be confirmed.

The clamp faces must grip the bare whistle without a liner. A CAD closure check
shows the seat contacts before the faces bottom, but it does not establish grip
force. Tighten only enough to prevent movement and inspect the brass for marks.
The rail, clamp and hinge geometry must preserve finger access, especially over
the hole above the keyed hole.

## Materials and printing

- Frame, keys, caps and EVA cutting guide: PETG. Every printed part is PETG.
- Pads: 2.0 EVA foam sheet, cut from the supplied guide; not printed.
- Pins: friction-fit 1.0 × 12 steel dowels.
- Springs: nominal 2 × 5 compression coils.
- Adhesive: compatible with the selected PETG and EVA; thin glue layer.

Use the supplied P1S 3MF orientations. The frame and keys are printed with
their specified supports; the cutting guide is flat-base-down and
support-free. Print three identical keys. The single-plate 3MF holds the same
PETG parts as the two-plate project.

## Acceptance requirements

Automated CAD checks should verify:

- all three independent hole positions and common interchangeable geometry;
- valid closed solids and STEP/STL round trips;
- 21 sampled positions through the full 35° travel;
- key, pad, frame, tube and cap collision clearance;
- actual opening-stop contact and overtravel interception;
- open airway clearance;
- spring solid-height and preload margins, plus hinge/collar clearance;
- pin insertion path and bearing fit;
- sealing coverage around all three holes;
- pad tabs, ring notches and full pad seating;
- clamp, bolt-head and M2 nut-pocket geometry.

Physical trials remain required for print strength, pin insertion effort, spring
return, opening/closing force, clamp grip, EVA adhesion, airtight sealing,
finger clearance, fatigue and sound. Specifically compare each open note with
the unkeyed whistle; the 35° CAD clearance is not proof that the pad has no
acoustic effect.

## Restart checklist

Start from `scripts/three_key.py`, set the measured hole table and 14.2 tube
OD, then rebuild through the build123d MCP workflow. Regenerate the three-key
build and both 3MF projects, run `tests/test_three_key.py` and
`tests/test_package_3mf.py`, validate the printable parts, and inspect the
assembly STEP. Do not silently reuse older 20° or widened-carrier exports.

