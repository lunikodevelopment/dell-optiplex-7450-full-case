# V3 revalidation report

## Requested corrections

| Requested item | V3 result |
|---|---|
| Discard old Dell-side STL | Done. New receiver generated from scratch. |
| <= ~140 x 140 mm Dell-side envelope | 138 x 138 mm. |
| Retain 100 x 100 M4 | Yes. |
| 25–30+ mm wall clearance | Nominal Dell-rear-to-wall spacing is 52.3 mm; nominal enclosure-back-to-wall spacing remains 45.5 mm. |
| Broad two-piece or steel-stud interface | Four M8 steel studs on a 76 x 56 mm pattern. |
| Positive anti-lift screw | Removable lock block closes the release channel and is retained by one M5 screw. |
| 9–10 mm critical receiver thickness | 10 mm uniform structural section. |
| Larger load-spreading washers | Designed around ~20 mm OD M4 fender washers. |
| Explicit wall pattern | 3-hole vertical stud centerline + 190 x 120 mm masonry pattern, with drill template. |
| 2–3 mm cheap fit template | 2.5 mm receiver/recess template. |
| H2C compatibility | Dedicated H2C enclosure set; all H2C/universal/fit STL envelopes automatically checked against 300 x 315 x 315 mm. |
| Efficient SLS/MJF version | Dedicated 2-rear-half + 2-front-half set. |

## Additional issues rechecked for the complete enclosure

- **Load-path separation:** shell is not connected to wall plate and cannot be the intended carrier.
- **Keyhole direction:** entry circle is below the final M8 shank position; receiver lowers 14 mm to seat.
- **Lock/install contradiction:** fixed by using a removable lock block installed only after seating. The wall ear's path stays open during entry.
- **Ventilation:** rear is primarily open; top exhaust region is broadly opened; central mount region remains open.
- **Left-side I/O:** broad side aperture rather than guessed individual connector cutouts.
- **Right-side optical/OSD/power:** broad side aperture rather than guessed coordinates.
- **Rear I/O/cables:** open rear architecture and bottom service window.
- **Camera/privacy controls:** 180 mm top-center front relief.
- **Bottom front features:** 400 mm bottom-center relief.
- **Unknown Dell rear curvature:** no attempt to conform tightly; 2.5 mm XY and 4 mm depth allowances plus mandatory corner coupon.
- **M4 usable depth:** intentionally unresolved; screw length must be measured on the actual unit.
- **Thermal behavior:** still physically unverified. Do not close the large openings until temperatures have been measured under load.
- **FDM creep:** structural receiver should use creep-resistant engineering material; optional 2 mm metal backer is included for permanent mounting.
- **Manufacturing method:** geometry is split separately for H2C and large-format powder-bed processes rather than forcing one inefficient segmentation on both.

## Automated CAD checks

See `QA_RESULTS.json`. It records exported STL dimensions, watertightness, H2C envelope checks and the main design invariants.

## Not a certified load rating

The design has intentionally conservative geometry and steel hardware, but no generated STL is a certified wall-mount product. Proof-load the assembled interface with a nonvaluable dead load before installing the computer, and use a secondary safety tether for a permanent installation.
