# Dennis WX — Northwoods Weather Command

A prototype weather dashboard built for Dennis: self-taught meteorologist, snowmobiler,
boater, and serious pickle person. One file, no build step, no dependencies.

**Open it:** double-click `index.html`, or serve the folder (`python3 -m http.server`)
and visit `http://localhost:8000`.

## What's in it

- **Live conditions** — temperature, feels-like, wind and gusts, humidity, dew point,
  barometric pressure, cloud cover, and visibility, for any town you search.
- **The Dennis Indices** — three homemade readiness gauges scored 0–100:
  - **Sled Index** (snowmobiling): trail temperature, new snow over the next 3 days, wind, visibility.
  - **Boat Index** (big water): air temperature, sustained wind, gusts, and the 6-hour rain chance.
  - **Brine Index** (pickle integrity): humidity, dew point, and barometric steadiness. Yes, really.
- **24-hour plot** — temperature line with a hover crosshair and per-hour readout, plus a
  chance-of-precipitation strip sharing the same time axis.
- **Hourly forecast** — a swipeable 48-hour strip: conditions icon, temperature, feels-like,
  chance of precipitation, and wind for every hour, with sunrise and sunset dropped into the
  timeline where they fall and a slim divider at each change of day.
- **Wind compass** — direction needle with a gust ring that grows with the gusts.
- **Seven-day outlook** — highs, lows, a hi/lo range bar, precip chance, and snowfall totals.
- **Dennis's almanac** — trail, ramp, and brine notes written from the live numbers.
- **Animated sky** — snow, rain, drifting haze, or a starfield, picked from the current
  weather code. Honors `prefers-reduced-motion`.
- Location search, browser geolocation, °F/°C toggle, and both remembered across visits.

## Data

Live observations and forecasts come from the [Open-Meteo](https://open-meteo.com) public
API — no key, no account. Place search uses the matching Open-Meteo geocoding endpoint.

If the network is unavailable, the page falls back to a **modeled demo day** that follows the
current season, flags itself as demo data in the header, and keeps every feature working.
That makes the prototype safe to open on a plane, a job site, or a locked-down laptop.

## Notes on the build

- Single self-contained `index.html`: markup, CSS, and JS in one file.
- Charts are hand-drawn SVG, re-rendered on resize — no charting library.
- Data colors were validated for color-vision deficiency and contrast against the dark
  surface; the gauges pair every color with an icon and a word, so nothing is carried by
  color alone.
- Responsive down to phone width, with no horizontal scrolling.

The indices are heuristics that Dennis is welcome to argue with — they are not official
forecasts. Check the National Weather Service before actually heading out on the ice.
