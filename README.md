# Dell OptiPlex 7450 AIO Full Enclosure — V3.1 Clearance-First

> [!IMPORTANT]
> **AI-authorship disclosure:** This CAD project and its documentation were generated with **OpenAI ChatGPT (GPT-5.6 Sol)** from Dell specifications, user-supplied photographs, independent product photographs, and iterative requirements. The CAD source, exported geometry, QA scripts/results, and engineering recommendations are AI-generated. This is **not a certified engineering product** and has not been physically validated on every Dell OptiPlex 7450 AIO.

V3.1 is the **pre-purchase / clearance-first** revision. It intentionally gives up a small amount of cosmetic tightness to remove dependence on unpublished Dell dimensions while retaining the full enclosure concept, wall mounting, H2C compatibility, and efficient SLS/MJF production.

## What changed from V3

- Dell receiver reduced from **138 × 138 mm to 128 × 128 mm**.
- Receiver remains **10 mm structurally thick** with 6 mm Dell-side standoffs.
- VESA remains the official **100 × 100 mm M4** pattern.
- Steel wall-stud/keyhole pattern widened to **84 × 56 mm**.
- Bottom-center receiver opening widened to **56 mm** and extended to the edge so the stand latch/mechanism is not trapped behind a flat plate.
- Positive anti-lift geometry corrected: seated clearance is **1.0 mm**, with no block/ear intersection, while only 1 mm of lift is available before the lock stops motion versus 14 mm required to release the keyholes.
- Enclosure body clearance increased to **5 mm per side** (10 mm total X/Y).
- Rear/depth clearance increased to **8 mm** beyond Dell's maximum published chassis depth.
- Front retention overlap reduced to **2 mm** per edge.
- Central shell exclusion increased to **190 × 190 mm**.
- Side I/O, optical-drive/control, rear-port and top-exhaust regions remain broadly open instead of depending on guessed port coordinates.
- All H2C parts remain inside the conservative **300 × 315 × 315 mm** design envelope; largest generated H2C part is about **295.62 × 210.45 × 74.3 mm**.

## Published Dell basis

- Chassis: **575.24 × 392.90 × 63.50 mm maximum published depth**.
- VESA: **FDMI MIS-D 100 × 100 mm, M4**.
- Minimum wall clearance: **20 mm**.
- V3.1 nominal Dell-rear-to-wall distance: **52.3 mm**.
- V3.1 nominal printed-shell-to-wall clearance: **41.5 mm**.

## Photo-derived rear-bay cross-check

The supplied near-orthogonal rear photograph contains the same four VESA threaded centers whose spacing is independently published as 100 mm. Using that known spacing as an image scale gives an approximate visible stand bay of **145.5–149.3 mm wide** and about **150.9 mm high**.

This is not metrology-grade because of perspective and edge ambiguity, but it gives the 128 mm receiver roughly **8.7–10.7 mm lateral clearance per side** and roughly **11.5 mm top/bottom clearance** against the visible bay boundary. The new 56 mm open-bottom notch additionally avoids the prominent stand latch visible below the lower M4 pair.

Independent rear photographs and genuine Dell 7450VESA bracket photographs corroborate the same bay/latch/bracket arrangement, although no dimensioned engineering drawing of the exterior recess or usable M4 thread depth was found. See `ONLINE_SOURCE_NOTES.md` and `REVALIDATION_V3_1.md`.

## Repository layout

Current source/build files:

- `source_parts_v3_1/` — chunked canonical V3.1 CadQuery source used by CI.
- `build_v3_1.py` — reconstructs `CAD_SOURCE_make_v3_1.py` and builds the CAD.
- `CAD_SOURCE_make_v3_1.py` — generated complete source file after CI runs.
- `.github/workflows/generate-cad.yml` — automatically regenerates production files.

Generated production files are committed under `generated/`:

- `generated/sls_mjf/` — **2 rear halves + 2 front halves** for large-format SLS/MJF PA12.
- `generated/h2c/` — **4 rear quadrants + 4 front quadrants** for H2C-class FDM.
- `generated/universal/` — structural receiver, wall plate, anti-lift block and seam joiners.
- `generated/fit_checks/` — inexpensive validation templates/coupons.
- `generated/optional_metal/` — optional 2 mm receiver backer in STL/STEP/DXF form.
- `generated/case_reference_assembly.step` — enclosure reference assembly.
- `generated/wall_interface_entry.step` / `generated/wall_interface_seated.step` — wall-interface kinematic references.

## Manufacturing paths

### H2C / large-format FDM

Use the `generated/h2c/` set. The enclosure quadrants are sized to stay under a conservative 300 × 315 × 315 mm envelope. A single nozzle/material is sufficient. See `H2C_PRINT_PLAN.md`.

### SLS / MJF

Use the `generated/sls_mjf/` set for the lowest assembly count: two rear shell halves and two front-retainer halves. PA12 or comparable functional nylon is preferred. See `SLS_MJF_PLAN.md`.

## Structural system

The printed enclosure is deliberately **not the primary wall-load path**. The Dell's VESA connection transfers through the 128 × 128 × 10 mm receiver to four steel M8 studs and the wall plate.

The receiver includes:

- 100 × 100 mm M4 Dell interface;
- approximately 20 mm OD fender-washer bearing areas;
- 84 × 56 mm four-stud pattern;
- 14 mm gravity seating travel;
- broad open-bottom latch relief;
- removable positive anti-lift block secured by an M5 fastener.

For a permanent installation, the optional 2 mm metal receiver backer or a commercial metal VESA backbone is strongly preferred.

## Fit checks

The design is intentionally much less dependent on unpublished Dell geometry, but the repository still includes cheap validation parts:

1. `generated/fit_checks/vesa_recess_fit_template_2p5mm.stl`
2. `generated/fit_checks/m8_keyhole_and_insert_coupon.stl`
3. `generated/fit_checks/enclosure_corner_depth_coupon.stl`
4. `generated/fit_checks/enclosure_front_corner_coupon.stl`
5. `generated/fit_checks/front_overlap_1_2_3mm_coupon.stl`
6. `generated/fit_checks/wall_drill_template_2mm.stl`

The **M4 screw length / usable thread depth remains unpublished**. Do not choose final screw length solely from this model.

## QA status

See `QA_RESULTS.json` and `REVALIDATION_V3_1.md`.

Current generated V3.1 checks include:

- receiver outline ≤140 mm: PASS;
- structural receiver thickness 9–10 mm: PASS;
- nominal shell-to-wall clearance ≥20 mm: PASS;
- wall/receiver collision in seated state: **0 mm³**;
- wall/receiver collision in entry state: **0 mm³**;
- positive lock collision-free when seated: PASS;
- lock prevents lift-off before 14 mm keyhole release travel: PASS;
- all exported STL meshes watertight: PASS;
- all H2C production parts inside the conservative envelope: PASS.

These are CAD/mesh checks, not certification of wall substrate, fasteners, printed-material strength, creep life, thermal behavior, or manufacturing variation in a used AIO.
