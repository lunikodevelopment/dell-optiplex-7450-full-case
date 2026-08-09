# Dell OptiPlex 7450 AIO full enclosure — V3

> [!IMPORTANT]
> **AI-authorship disclosure:** This project was written and CAD-generated with **OpenAI ChatGPT (GPT-5.6 Sol)** from user-provided requirements, constraints, photographs, and iterative feedback. The documentation, parametric CAD source, exported geometry, validation scripts/results, and design recommendations are AI-generated. It is **not a certified engineering product** and has not been physically validated on the target Dell OptiPlex 7450 AIO unless a section explicitly says otherwise. Perform the included fit checks and use appropriate engineering judgment before supporting equipment from a wall.

V3 is a manufacturing-method-aware redesign of a complete protective enclosure and wall-mount system for the Dell OptiPlex 7450 AIO. It provides both an efficient large-format SLS/MJF layout and an H2C-compatible FDM layout from the same parametric CAD.

## Repository layout

Generated production files are committed under `generated/`:

- `generated/sls_mjf/` — **2 rear halves + 2 front halves** for large-format SLS/MJF PA12.
- `generated/h2c/` — **4 rear quadrants + 4 front quadrants** kept inside a conservative **300 × 315 × 315 mm** envelope.
- `generated/universal/` — structural receiver, wall plate, positive anti-lift lock and seam joiners used with either process.
- `generated/fit_checks/` — inexpensive validation templates/coupons that should be printed first.
- `generated/optional_metal/` — optional 2 mm receiver backer in STL/STEP/DXF form.
- `generated/case_reference_assembly.step` — full-case reference assembly.
- `generated/wall_interface_entry.step` and `generated/wall_interface_seated.step` — wall-interface kinematic references.

The parametric generator is assembled as `CAD_SOURCE_make_v3.py`. `build_v3.py` reconstructs it from `source_parts/` and regenerates the production files. GitHub Actions runs the same build automatically when the CAD source changes.

### Rebuild locally

```bash
python -m pip install -r requirements.txt
python build_v3.py
```

The regenerated files are written to `generated/`.

## Verified Dell basis

- Published chassis envelope used: **575.24 × 392.90 × 63.50 mm**.
- VESA: **100 × 100 mm, M4**.
- Dell minimum wall clearance basis: **20 mm**; V3 nominally places the Dell rear surface about **52.3 mm** from the wall before accounting for real recess curvature.
- The enclosure projects about 6.8 mm behind the published Dell maximum rear surface, leaving a nominal shell-to-wall gap of about **45.5 mm**.

## Structural receiver — corrections carried into V3

The Dell-side receiver was rebuilt rather than inherited from V1:

- **138 × 138 mm** main outline, under the requested ~140 × 140 envelope.
- **10 mm uniform structural thickness** at the steel-stud/keyhole load path.
- Four **100 × 100 M4** Dell holes.
- Flat wall-facing washer seats sized for approximately **20 mm OD M4 fender washers**; no deep counterbores weaken the receiver.
- Four broad steel-stud keyholes arranged **76 × 56 mm** using **M8 steel studs**. Entry circles are below the final seated positions; the receiver lowers **14 mm** to seat.
- Four **6 mm Dell-side standoffs**, keeping stud hardware away from the Dell rear cover.
- Open central relief for stand latch/recess avoidance.
- **Positive anti-lift system:** a wall ear travels in the receiver's open-bottom center channel. After seating, insert the positive anti-lift lock block and secure it with one M5 screw. The block physically closes the release path below the wall ear, so lift-off requires removing the screw and block first.

The lock block is separate on purpose: it keeps the keyhole entry path fully open during installation and removes the geometry contradiction present in the early design.

## Mandatory fit-check sequence

1. Print `generated/fit_checks/vesa_recess_fit_template_2p5mm.stl` in cheap PLA.
2. Loosely bolt it to all four Dell M4 positions with washers. Confirm the **entire 138 × 138 outline** clears the molded recess, latch and casing. Do not force it flat.
3. Verify the central relief clears the latch/mechanism.
4. Print `generated/fit_checks/m8_keyhole_and_insert_coupon.stl` and test the exact M8 washer/head stack and any brass inserts you plan to use.
5. Print `generated/fit_checks/enclosure_corner_depth_coupon.stl` and `generated/fit_checks/enclosure_front_corner_coupon.stl` and check edge/depth clearance.
6. Use `generated/fit_checks/front_overlap_3_4_5mm_coupon.stl` to confirm that 4 mm front retention does not intrude into the active display, speaker grille or controls.
7. Only after these checks pass should the paid SLS/MJF shell or structural H2C parts be ordered/printed.

## Wall attachment

`generated/universal/wall_plate_4xM8_stud.stl` is 220 × 160 mm and explicitly contains:

- timber-stud centerline holes at y = -60, 0, +60 mm;
- masonry pattern corners at **190 × 120 mm**;
- four M8 carriage-bolt / steel-stud bosses matching the 76 × 56 mm receiver interface.

Use wall fasteners appropriate to the actual substrate. Printed-plastic strength does not compensate for inadequate drywall/plasterboard anchors.

## Full enclosure improvements and revalidation

The printed enclosure is intentionally **not part of the AIO's structural wall load path**. It traps/protects the chassis while the Dell's metal VESA interface carries the computer.

- 3.0 mm perimeter shell walls and 2.8 mm rear bands are efficient for SLS/MJF and remain straightforward for FDM.
- Rear center has a **184 × 184 mm structural avoidance opening**, much larger than the 138 mm receiver.
- Rear surface is mostly open instead of being a solid sheet with guessed ventilation slots.
- Left side has a broad service opening for the documented card reader, USB-C, USB and headset connections.
- Right side has a broad service opening for the documented optical drive, OSD buttons and power controls.
- Top rear is broadly open so the long exhaust region is not boxed in.
- Rear remains open around the power/network/USB/HDMI/DisplayPort/audio region.
- Top-center front retainer is relieved for camera/microphones/privacy latch.
- Bottom-center front retainer is broadly relieved to reduce the risk of blocking speakers/service features.
- Enclosure seams are nonstructural and use simple M3 joiner bars.

## H2C notes

The H2C production set uses four rear quadrants and four front quadrants. Use a **single nozzle/material for each component**; no multi-tool printing is required. For FDM, the shell should be treated as a low-infill enclosure, while the receiver and wall plate should use a creep-resistant engineering material and conservative structural settings.

The CAD QA records the largest H2C enclosure part as approximately **293.12 × 207.95 × 70.3 mm**, within the project's conservative 300 × 315 × 315 mm target. Verify the actual service's selected H2C tool/nozzle mode in the slicer before committing a batch.

See `H2C_PRINT_PLAN.md` and `generated/QA_RESULTS.json`.

## SLS/MJF notes

The SLS/MJF set minimizes seams: two rear halves and two front halves. The full-height halves are approximately 416 mm long, so the manufacturing service must confirm its build envelope and tolerance for long PA12 parts.

See `SLS_MJF_PLAN.md`.

## Hardware summary

- Dell: 4 × M4 VESA screws of **physically verified length** + ~20 mm OD fender washers.
- Wall interface: 4 × M8 steel carriage bolts/studs, M8 washers and locking nuts.
- Positive lock: 1 × M5 screw + M5 square nut for the removable anti-lift block.
- Enclosure: M3 screws/washers/nuts for seams; M3 threaded inserts or service-selected equivalent for front retainer tabs.
- Wall fasteners: substrate-specific, not included in the CAD assumption.
- Optional: 2 mm aluminum receiver backer and a secondary steel safety tether.

See `BOM.md` for the concise hardware list.

## Validation status

Automated CAD checks are published in `QA_RESULTS.json` and regenerated in `generated/QA_RESULTS.json`. They include watertightness, H2C bounding-envelope checks, receiver dimensions, wall clearance, collision checks for the entry/seated wall interface and positive-lock travel.

This does **not** constitute a certified load rating. Proof-load the assembled wall interface with a nonvaluable dead load before installing the computer, and use a secondary safety tether for a permanent installation.

## Still requires physical verification

Published specifications do **not** provide the stand-recess width/depth, usable M4 thread depth, exact rear curvature, exact port coordinates, optical-drive protrusion, active-screen edge location, or thermal temperatures inside a close enclosure. V3 addresses these unknowns with avoidance openings and fit coupons, but they cannot be truthfully declared solved until the actual AIO is checked.

See `MEASUREMENT_CHECKLIST.md` before ordering an expensive final enclosure.
