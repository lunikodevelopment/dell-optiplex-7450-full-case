# H2C manufacturing plan

Official H2C specifications provide a build volume larger than these parts, but tool/nozzle mode can change the usable X range. V3 therefore uses a deliberately conservative per-part target of **300 x 315 x 315 mm**.

Recommended part set:

1. `rear_top_left`
2. `rear_top_right`
3. `rear_bottom_left`
4. `rear_bottom_right`
5. four matching front retainer quadrants
6. universal receiver, wall plate and anti-lift block

Print the shell pieces with their broad rear plane/edge arrangement selected to minimize supports in the service's slicer. The geometry uses large open windows rather than support-heavy duct tunnels.

For lowest printing time, use a 0.6 or 0.8 mm nozzle if the service supports it and accepts the resulting surface finish. Shell walls are 3.0 mm nominal; do not enable dense infill simply because earlier P1S revisions used it. The structural receiver/wall plate are compact and should receive the conservative structural settings, not the whole enclosure.
