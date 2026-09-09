# Key arm reinforcement — 9 September 2026

The user reported broken keys and supplied a photo showing an intact pad cup and TPU pad with a short arm fragment still attached. The photo supports investigating the curved arm; it does not establish the exact fracture plane, loading history or whether layer adhesion contributed.

The upper arm now grows from the existing 4 mm width to 6 mm between Z = 5.5 and 7.5 mm. Up to 1 mm of radial stock is added on the outside of the curve, giving a 4 mm radial section in the fully reinforced region. The reinforcement starts at Z = 3.4 mm, above the fixed bearing heads, and tapers into the original profile. The cup's top height and pad seat are retained.

The hinge hub, pin bore, opening-stop tail, spring peg, spring interfaces and pad geometry are unchanged. All three keys use the same geometry. Numerical comparison with the previous key found no removed material; added stock lies between Z = 3.4 and 12.095 mm, on the upper arm. Key volume increases from 658.4710 to 732.4115 mm³, about 11.2%.

MCP solid validity and STEP export gates pass. Printability analysis reports two overhang warnings and one thin-wall warning, with no errors. The existing print package retains supports for the keys, four walls and 0.16 mm layers. This report does not certify the reinforcement's physical strength. The first replacement should be trialled in the existing frame before relying on a full set.

The regression suite checks actual added stock at two bend sections, the existing 4 mm hinge envelope, full key travel, spring and pin access, pad seating, interchangeability and exports. The accompanying image shows original material in blue and added material in red.

Validation completed: the 20 existing three-key tests passed. The new reinforcement test passed after correcting its handling of a multi-piece section result; no geometry change was needed for that test correction. All four print-package tests also passed.

## Continuous hinge-bore collar

The user identified the thin spring-facing side of the key's hinge bore. The spring-clearance cut left only 0.475 mm between the 1.25 mm bore and the straight edge. A full annular collar is now restored after those cuts: 1.525 mm outside radius minus 0.625 mm bore radius gives at least 0.9 mm radial stock across the full 4 mm bearing length.

This requires a matching frame. Both the moving spring peg/seat and fixed socket move from Z = 2.6 to 2.9 mm, providing room for the collar and retaining material beneath the socket. The sloping underside of the fixed socket is positioned from the collar radius and a 0.2 mm clearance requirement. Measured collar/frame clearance is 0.20433 mm, and the vertical material beneath the socket mouth is 0.68483 mm. The flush back and connections to both bearing pillars remain.

The steel pin remains 1 × 12 mm; the moving bore remains 1.25 mm, fixed bores remain 1.1 mm and pads/clamp caps are unchanged. Use the revised keys and revised frame together. Closed spring length remains 2.8 mm; the calculated open length changes from about 3.697 to 3.800 mm, below the assumed 5 mm free length. The changed spring height can affect feel and needs physical evaluation.

Key volume is 732.9761 mm³; frame volume is 6578.6130 mm³. Both pass MCP validity and STEP export gates. Printability findings remain three warnings for a key and eleven for the frame; existing support settings are retained. Strength and fit still require a printed trial.

The new regression verifies a complete 0.9 mm annular wall, at least 0.2 mm clearance from the frame, and at least 0.2 mm from the spring envelopes at all 21 sampled positions through the key travel (measured minimum 0.26566 mm). Existing full key-travel and interface tests also apply.

Final validation: all 22 three-key geometry tests and all four print-package tests passed with the spring at Z = 2.9 mm. The initial 2.8 mm trial was rejected because the open spring envelope had only 0.1695 mm clearance; the delivered geometry meets the 0.2 mm requirement across the sampled travel.
