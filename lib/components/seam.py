"""Scroll-sewn seam animation.
There is no server-rendered markup: src/js/seam.js draws the straight stitch line and needle into a fixed SVG layer,
styled by src/css/30-animations.css, and the content keeps clear of it via the 'seam lane' padding in 03-layout.css.
This module only documents the component and exposes its settings for reference."""
SETTINGS = {"desktop_stitch_px": 14, "desktop_gap_px": 9, "mobile_stitch_px": 10, "mobile_gap_px": 7, "lane_padding_mobile_px": 28}
