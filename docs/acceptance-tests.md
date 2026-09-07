# Engineering and usability acceptance tests

These requirements distinguish CAD checks from evidence obtained with an actual
print and the player's whistle. Numerical margins below are provisional
engineering targets for this prototype, not clinically established values.

## Automated engineering checks

| ID | Requirement | Evidence / pass criterion |
|---|---|---|
| E01 | The mechanism reaches open and closed stops without unintended collision. | At 21 equally spaced positions, rigid key clears frame/tube; pad clears frame and fits its locator. Intersection volume below 0.00001 mm³. Intended pad/brass compression is excluded. Sampling is not a continuous sweep proof. |
| E02 | The clamp body does not occupy the brass tube or its other half. | Nominal frame/cap/tube intersections below 0.00001 mm³. Actual lining compression and grip are physical tests. |
| E03 | The spring returns the key and is not driven solid. | Open spacing less than 5 mm free length; closed spacing greater than assumed 2 mm solid plus 0.5 mm margin. This establishes preload displacement, not adequate return force. |
| E04 | The pin spans both supports and does not bind the moving key geometrically. | At least 0.5 mm pin projection at each end; no pin/key solid intersection and positive nominal bore clearance. Printed friction/running fits are physical tests. |
| E05 | Parts can be exported as printable closed solids. | One valid positive-volume solid per part; flat bed-contact area over 10 mm²; STEP round-trip volume within 0.0001%; watertight, consistently wound STL with volume within 1%. These checks do not prove slicability or adhesion. |
| E06 | The open pad/key do not occupy the immediate airway above the hole. | The hole's vertical projected opening stays clear through 1 mm above the tube crown. This is a geometric proxy; it does not guarantee unchanged tone or tuning. |
| E07 | The closed pad offers a continuous nominal sealing band around the hole. | Probe three concentric paths, 1.5–2.0 mm beyond the hole radius, at 5° intervals and 0.1 mm radial interference. Each point must lie within pad material. This does not establish real airtightness. |
| E08 | The pad's locating recess does not puncture its roof. | Sample at least 1 mm of solid material below the socket across its footprint. No through-hole is allowed above the whistle opening. |

These checks operate on regenerated geometry, not on hard-coded part volumes.
For example, E01 exposed a collision between the curved pad and the original
spring seat. Narrowing and moving the seat addressed that actual obstruction. E06 also
exposed the curved lip occupying the airway at 4 mm lift. Increasing the
prototype lift to 6 mm clears the specified region; the extra travel remains
subject to the player’s comfort trial.

The measured-instrument revision also checks a 1 mm axial margin between the
lower clamp and hole 5, using the still-provisional 6 mm hole 5 diameter.

The continuous-face revision additionally probes material across the centre
of the curved contact face to prevent reintroducing the rejected central relief.
The sealing-band check still applies to the outer region of this full face.

## Physical usability and function tests

Record outcomes for the right index finger first. Use the actual playing grip,
whistle, spring and pad. Do not infer any of these passes from CAD.

| ID | Requirement | Practical test and acceptance |
|---|---|---|
| U01 | The hole stays fully open under the player's unintentionally resting finger. | Rest the finger naturally on the contact while playing notes requiring the hole open. The key remains at its open stop and produces no unwanted muffling. |
| U02 | Closing is deliberate and comfortable. | Play a familiar passage with repeated closures. The player can reliably close and release without excessive effort or unacceptable fatigue. Duration and repetition count remain to be agreed with the player. |
| U03 | Closed notes seal reliably. | Compare low notes with normal finger sealing and with the key. No leak-induced weak response or instability at comfortable pressure, including after repeated closures. |
| U04 | Open-note sound is preserved. | Compare with the attachment removed and installed, including a resting finger. No player-objectionable change in response, tone or pitch. A numerical cents tolerance has not been agreed. |
| U05 | Mounting remains secure and does not mark the instrument. | Play normally, then inspect alignment, liner, brass and remaining clamp gap. No observable slip, marking or need for excessive bolt tension. |
| U06 | Other fingers and grip remain usable. | Play passages using the two uncovered right-hand holes. Clamps and rail do not obstruct fingering or force an uncomfortable grip. |
| U07 | The mechanism remains serviceable. | After repeated operation, check pin migration, return to stop, pad attachment, spring seating and wear. Cycle count and acceptable wear limits are not yet specified. |

## Force measurements to establish later

Measure force at the actual finger contact, including initial movement and full
closure, rather than quoting spring force alone. Useful eventual criteria are:

- Opening resistance exceeds the player's resting finger load by an agreed margin.
- Closure force stays within the player's comfortable deliberate force range.
- Return overcomes friction without finger assistance.

Those loads, margins and a suitable measurement method remain unestablished.
They are deliberately not assigned arbitrary Newton thresholds in CI.

## Trial record

For each trial record date, model commit, measured whistle dimensions, printer
profile, PETG/TPU brand and condition, spring identity, pin-coupon outcome,
adhesive/liner choice, and results for U01–U07. Record failures and changes as well
as passes. Extend to three keys only after the single-key results are acceptable
to the player.
