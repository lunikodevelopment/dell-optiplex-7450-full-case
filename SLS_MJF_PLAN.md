# SLS / MJF manufacturing plan

Use `sls_mjf/` when the provider accepts a roughly 293 x 404 x 70 mm rear half. This reduces the protective enclosure to four major printed pieces: two rear halves and two front halves.

The shell is modeled as real 3.0 mm walls / 2.8 mm rear bands with open service regions, so there is no FDM-style infill to pay for. Large internal openings also reduce powder/material volume and make cleaning easier.

Ask the provider to confirm:
- machine bounding box for the full-height halves;
- PA12 dimensional tolerance on ~400 mm long parts;
- preferred minimum wall/rib thickness;
- whether they recommend splitting the full-height halves further to reduce warp/cost.

If the provider rejects the large halves, use the H2C quadrant STL set with SLS/MJF as a universally smaller fallback.
