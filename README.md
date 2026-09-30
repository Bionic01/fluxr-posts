# Fluxr posts

Daily Facebook/Instagram posters for Fluxr, made in code (no AI images) with the approved logos.

- `kit/render.py` builds a 1080x1350 poster from a small JSON config (see the docstring and `kit/examples/`).
- `kit/logos/` holds the approved Fluxr, voucher and network logos (from "Fluxr Approved Logos").
- `posts/` holds each day's finished poster. Metricool and Meta ads load them from their public raw URL.

Render: `cd kit && python3 render.py examples/sample_zw.json ../posts/test.png`
