# TIDEGLASS departure board

A responsive, single-page harbour departure briefing built as a fictional public-information demonstration.

## Run locally

No installation or build step is required. Open `index.html` directly in a browser, or serve this folder with any static file server.

For example:

```sh
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Interactions

- Select **Now**, **07:00**, or **09:00** to compare the decision, wind, gust, and swell readings. Arrow keys, Home, and End work within the selector.
- Mark the four pre-departure checks to update the completion count.
- The notice form validates locally and never transmits or stores its value. Submit a valid address for the success preview, or `fail@example.test` for the failure preview.

All content is demonstration data and must not be used for navigation.
