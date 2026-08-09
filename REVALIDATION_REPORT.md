# V3.1 Revalidation Report

V3.1 replaces the previous receiver geometry with a clearance-first layout based on published Dell dimensions plus photographic cross-checking.

## Confirmed online

- Dell external envelope: **575.24 × 392.90 × max 63.50 mm**.
- VESA: **100 × 100 mm, M4**.
- Dell minimum wall clearance: **20 mm**.
- The removable stand exposes the central stand/VESA bay.
- Rear, side and top I/O/vent/control regions correspond with the broad openings used by this enclosure.

## Not published as dimensioned drawings

- exact stand-recess width/height/depth;
- exact rear curvature;
- exact latch protrusion;
- exact usable M4 thread depth;
- exact port coordinates and active-display edge offsets.

## V3.1 changes that reduce dependence on those unknowns

- receiver reduced to **128 × 128 mm**;
- **56 mm open-bottom notch** around the latch region;
- **6 mm Dell-side standoffs** around the M4 points;
- **5 mm clearance per X/Y side** and **8 mm extra depth clearance**;
- front overlap reduced to **2 mm**;
- **190 × 190 mm** central shell exclusion area;
- side, rear and top service/vent regions kept broadly open.

## Photo-derived cross-check

Using the known 100 mm VESA spacing in the supplied near-orthogonal rear photograph as an image scale gives an approximate visible bay width of **145.5–149.3 mm** and height of about **150.9 mm**. A 128 mm receiver therefore has roughly **8.7–10.7 mm lateral clearance per side** and about **11.5 mm vertical clearance per side** against the visible bay boundary. These are photographic estimates rather than metrology-grade dimensions.

## CAD/mesh QA

- receiver envelope ≤140 mm: PASS;
- 10 mm structural receiver thickness: PASS;
- nominal Dell-rear-to-wall distance: **52.3 mm**;
- nominal printed-shell-to-wall clearance: **41.5 mm**;
- wall/receiver intersection in seated state: **0 mm³**;
- wall/receiver intersection in entry state: **0 mm³**;
- anti-lift block seated gap: **1.0 mm**;
- keyhole release travel: **14 mm**;
- all exported STL meshes watertight: PASS;
- H2C conservative envelope: PASS;
- largest H2C part: **295.62 × 210.45 × 74.3 mm**.

The remaining unknowns are individual-unit manufacturing condition and usable M4 thread depth. The design minimizes dependence on them, but those values are not available from a published Dell dimensioned drawing.
