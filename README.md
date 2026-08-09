# Dell OptiPlex 7450 AIO full enclosure — V3

> [!IMPORTANT]
> **AI-authorship disclosure:** This project was written and CAD-generated with **OpenAI ChatGPT (GPT-5.6 Sol)** from user-provided requirements, constraints, photographs, and iterative feedback. The documentation, parametric CAD source, exported geometry, validation scripts/results, and design recommendations are AI-generated. It is **not a certified engineering product** and has not been physically validated on the target Dell OptiPlex 7450 AIO unless a section explicitly says otherwise. Perform the included fit checks and use appropriate engineering judgment before supporting equipment from a wall.

V3 is a manufacturing-method-aware redesign. It replaces the old many-tile P1S shell with one master geometry exported in two efficient production sets:

- `sls_mjf/`: **2 rear halves + 2 front halves** for large-format SLS/MJF PA12. This is the lowest assembly-count printed version.
- `h2c/`: the same enclosure split into **4 rear quadrants + 4 front quadrants**. Every H2C part is deliberately kept inside a conservative **300 x 315 x 315 mm** bounding envelope, so it remains printable even if the selected H2C tool mode exposes less than the nominal maximum X travel.
- `universal/`: compact structural wall interface and seam joiners used with either process.
- `fit_checks/`: cheap validation parts. Print these before the expensive enclosure.
- `optional_metal/`: a 2 mm flat receiver backer (STEP/STL and DXF where exporter support is available). It is optional but recommended for a permanent wall installation.

## Verified Dell basis

- Published chassis envelope used: **575.24 x 392.90 x 63.50 mm**.
- VESA: **100 x 100 mm, M4**.
- Dell minimum wall clearance: **20 mm**, while V3 nominally places the Dell rear surface about **52.3 mm** from the wall before accounting for real recess curvature.
- The enclosure projects about 6.8 mm behind the published Dell maximum rear surface, leaving a nominal shell-to-wall gap of about **45.5 mm**.

## Structural receiver — corrections carried into V3

The Dell-side receiver was rebuilt rather than inherited from V1:

- **138 x 138 mm** main outline, under the requested ~140 x 140 envelope.
- **10 mm uniform structural thickness** at the steel-stud/keyhole load path.
- Four **100 x 100 M4** Dell holes.
- Flat wall-facing washer seats sized for approximately **20 mm OD M4 fender washers**; no deep counterbores weaken the receiver.
- Four broad steel-stud keyholes arranged **76 x 56 mm** using **M8 steel studs**. Entry circles are below the final seated positions; the receiver lowers **14 mm** to seat.
- Four **6 mm Dell-side standoffs**, keeping stud hardware away from the Dell rear cover.
- Open central relief for stand latch/recess avoidance.
- **Positive anti-lift system:** a wall ear travels in the receiver's open-bottom center channel. After seating, insert `positive_anti_lift_lock_block` and secure it with one M5 screw. The block physically closes the release path below the wall ear, so lift-off requires removing the screw and block first.

The lock block is separate on purpose: it makes the keyhole entry path fully open during installation and removes the geometry contradiction that affected the early design.

## Mandatory fit-check sequence

1. Print `fit_checks/vesa_recess_fit_template_2p5mm.stl` in cheap PLA.
2. Loosely bolt it to all four Dell M4 positions with washers. Confirm the **entire 138 x 138 outline** clears the molded recess, latch and casing. Do not force it flat.
3. Verify the central relief clears the latch/mechanism.
4. Print `m8_keyhole_and_insert_coupon.stl` and test the exact M8 washer/head stack and any brass inserts you plan to use.
5. Print `enclosure_corner_depth_coupon.stl` + `enclosure_front_corner_coupon.stl` and check edge/depth clearance.
6. Use `front_overlap_3_4_5mm_coupon.stl` to confirm that 4 mm front retention does not intrude into the active display, speaker grille or controls.
7. Only after these checks pass should the paid SLS/MJF shell or structural H2C receiver be ordered/printed.

## Wall attachment

`wall_plate_4xM8_stud` is 220 x 160 mm and explicitly contains:

- timber-stud centerline holes at y = -60, 0, +60 mm;
- masonry pattern corners at **190 x 120 mm**;
- four M8 carriage-bolt / steel-stud bosses matching the 76 x 56 mm receiver interface.

Use wall fasteners appropriate to the actual substrate. Do not treat printed-plastic strength as permission to use inadequate drywall/plasterboard anchors.

## Full enclosure improvements and revalidation

The printed enclosure is intentionally **not part of the AIO's structural wall load path**. It traps/protects the chassis while the Dell's metal VESA interface carries the computer.

- 3.0 mm perimeter shell walls and 2.8 mm rear bands are efficient for SLS/MJF and remain straightforward for FDM.
- Rear center has a **184 x 184 mm structural avoidance opening**, much larger than the 138 mm receiver.
- Rear surface is mostly open instead of a solid vented sheet.
- Left side has a large service opening for the documented card reader, USB-C, USB and headset connections.
- Right side has a large service opening for the documented optical drive, OSD buttons and power controls.
- Top rear is broadly open so the long exhaust visible on the unit is not boxed in.
- Rear is open around the documented power/network/USB/HDMI/DisplayPort/audio area.
- Top-center front retainer is relieved for camera/microphones/privacy latch.
- Bottom-center front retainer is broadly relieved to reduce risk of blocking speakers/service features.
- Enclosure seams are nonstructural and use simple M3 joiner bars.

## H2C notes

The H2C production set uses four rear quadrants and four front quadrants. Use a **single nozzle/material for each component**; no multi-tool printing is required. For an FDM service, the shell is best treated as a low-infill ribbed enclosure, while `vesa_receiver_138x138_10mm` and `wall_plate_4xM8_stud` should use a creep-resistant engineering material and conservative wall counts.

The current official H2C nominal build volume is larger than the V3 conservative per-part envelope, but verify the service's chosen nozzle/tool mode in Bambu Studio before committing a batch.

## SLS/MJF notes

The `sls_mjf` set minimizes seams: two rear halves and two front halves. The halves are about half the Dell width but the full ~404 mm height, so the service must confirm its machine's bounding volume. PA12 powder-bed printing is particularly suitable because no FDM supports are required inside the shell openings.

## Hardware summary

- Dell: 4 x M4 VESA screws of **physically verified length** + ~20 mm OD fender washers.
- Wall interface: 4 x M8 steel carriage bolts/studs, M8 washers and locking nuts.
- Positive lock: 1 x M5 screw + M5 square nut (inserted in receiver pocket) for the removable anti-lift block.
- Enclosure: M3 screws/washers/nuts for seams; M3 brass inserts or service-selected equivalent for the eight front retainer tabs.
- Wall fasteners: substrate-specific, not included in the CAD assumption.

## Still requires physical verification

Published specifications do **not** give the stand-recess width/depth, usable M4 thread depth, exact rear curvature, exact port coordinates, optical-drive protrusion, active-screen edge location, or thermal temperatures inside a close enclosure. V3 addresses these unknowns with avoidance openings and coupons, but they cannot be truthfully declared solved until the actual AIO is checked.
