# Weather and clothing in a field guide

Use when weather or clothing advice is requested; do not add a weather service to every guide automatically.

Associate forecasts with itinerary dates, place IDs, coordinates and local timezone. A day may include departure, transit and destination cities: use a neutral weather heading or label each role. A current-city forecast must never masquerade as the trip-date forecast. For dates outside the provider's supported horizon, show unavailable/not-yet-published rather than substituting today's forecast or unlabelled seasonal averages.

A compact home view can show only the applicable day's weather; a day page may provide folded daily details. Show observation/forecast date separately from fetch time when ambiguity is possible. Keep fetch time and an accessible manual refresh action in the header if the design calls for it. Display only verified fields; no made-up conditions, coordinates or hourly precision. Preserve legally required provider attribution even when the user wants a quieter interface.

Cache by location, timezone and requested date coverage. Keep usable cached rows visible while refreshing; a small status change should not insert a temporary block that moves the itinerary. Handle stale, offline, failed, partial and out-of-horizon responses explicitly. Weather failure must not block core reading. Do not repeatedly refetch on every focus event.

Clothing advice should derive from the actual day activities and locations, with a distinction between what to wear and what to carry. City temperatures are not mountain/lake forecasts. Reconcile early pickups, elevation, wind/rain, walking, religious-site dress and baggage limits without inventing live weather. Reference graphics from another year or route are inspiration, not authoritative dates or temperatures.

Reuse one day-clothing record across weather and packing; avoid competing copies. Fold per-day advice and preserve the user's requested module order. Clothing suggestions are not automatically checked packing items. Do not add named personal equipment or purchased insurance details to public defaults.

Verify a multi-city travel day, a day outside the forecast horizon, delayed refresh with existing rows, an offline failure and a mountain-versus-city distinction. Check light/dark/palette tokens and narrow-screen headers as well as forecast parsing.
