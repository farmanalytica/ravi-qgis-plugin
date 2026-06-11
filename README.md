# RAVI — QGIS plugin for vegetation-index time series & imagery

RAVI is a QGIS plugin by [FARM Analytica](https://www.farmanalytica.com.br) that
integrates **Google Earth Engine (GEE)** into QGIS for vegetation-index time
series, multispectral/SAR imagery download, terrain and soil products. It targets
students, researchers, farmers, and professionals in agriculture, land monitoring,
and environmental management.

- **Homepage:** https://www.raviqgis.org
- **Repository:** https://github.com/farmanalytica/ravi-qgis-plugin
- **Issues:** https://github.com/farmanalytica/ravi-qgis-plugin/issues
- **License:** GPL v2 or later (see [`LICENSE`](LICENSE))

## Features

| Domain | What it does |
|---|---|
| **Optical** (Sentinel-2) | Vegetation-index time series, per-point / per-feature analysis, cloud (SCL) filtering, image preview, composites, multispectral download |
| **SAR** (Sentinel-1) | Backscatter retrieval, date filtering, plotting, styled rendering |
| **Landsat** | Batch and super-resolution scene download via `agrigee-lite` |
| **DEM** | Digital Elevation Model catalog browse + download + hillshade/terrain rendering |
| **SYSI** | Synthetic Soil Image generation |
| **Climate** | NASA POWER climate series |
| **Auth** | GEE sign-in — personal OAuth **and** service-account key |

## Requirements

- **QGIS 3.x** (Python 3.11 / 3.12 / 3.13; QGIS 3.44 LTR ships 3.12)
- A **Google Earth Engine** account + a Cloud project with the Earth Engine API enabled
- Third-party Python deps (`earthengine-api`, `agrigee-lite`, `google-*`, …) are
  **provisioned automatically** on first launch — see
  [Dependency provisioning](#dependency-provisioning).

## Installation

Install from the QGIS Plugin Manager, or clone into the QGIS plugin directory:

```
<QGIS profile>/python/plugins/ravi-qgis-plugin
```

On first activation RAVI downloads its dependency bundle (or pip-installs as a
fallback), then prompts for Earth Engine sign-in.

---

## Architecture

RAVI follows a layered **MVC-style** design. The Qt UI never talks to the Earth
Engine SDK directly; all remote work flows through a service layer and runs on
background threads so the QGIS UI stays responsive.

```
                 QGIS  ──classFactory──▶  __init__.py
                                            │  (boots extlibs, then loads RAVI)
                                            ▼
                                         ravi.py  (RAVI plugin class)
                                            │  builds menu/toolbar action
                                            ▼
                                       ravi_dialog.py  (main dialog + sidebar)
                                            │
            ┌───────────────────────────────┼───────────────────────────────┐
            ▼                                ▼                                ▼
       view/  (Qt widgets)   ◀──▶   controllers/  (per-feature glue)   ──▶  managers/ (settings, datasets)
                                            │
                       ┌────────────────────┼────────────────────┐
                       ▼                                          ▼
                  services/  (GEE + data business logic)     tools/  (map tools: AOI draw, point capture)
                       │
                       ▼
                  workers/  (QThread — run services off the UI thread)
                       │  results emitted via Qt signals
                       ▼
                  renderers/  (style results into QgsRasterLayer / map layers)
```

### Layers

| Layer | Path | Responsibility |
|---|---|---|
| **Entry / bootstrap** | `__init__.py`, `ravi.py` | `classFactory` provisions deps then instantiates `RAVI`; the plugin class wires the QGIS menu/toolbar and opens the dialog. |
| **Dialog / shell** | `ravi_dialog.py`, `view/sidebar.py`, `view/styles.py` | Main window, navigation sidebar, shared styling. |
| **View** | `view/` | Per-feature panels (`optical`, `radar`, `landsat`, `sysi`, `auth`, …), dialogs, plots (`sar_plot`), custom widgets (`range_slider`). Pure Qt — no business logic. |
| **Controllers** | `controllers/` | One per feature (`auth`, `optical`, `sar`, `dem`, `landsat`, `sysi`). Translate UI events into service/worker calls and push results back to layers and views. |
| **Services** | `services/` | Business logic. `gee_service.py` owns all Earth Engine auth/init; feature services (`optical`, `sar`, `dem`, `landsat`, `sysi`, `aoi`, `nasa_power`) build EE queries and return plain data (DataFrames / dicts). |
| **Workers** | `workers/` | `QThread` subclasses that run a service call off the UI thread and emit `finished` / `failed` signals (e.g. `optical_worker`, `landsat_batch_worker`, `climate_worker`). |
| **Renderers** | `renderers/` | Turn results into styled QGIS layers (`base_maps`, `dem_renderer`, `sar_renderer`, `raster_renderer_utils`). |
| **Managers** | `managers/` | Cross-cutting state — `settings_manager` (QgsSettings), `dataset_manager` (catalogs). |
| **Tools** | `tools/` | QGIS map tools (`aoi_draw_tool`, `point_capture_tool`) and the vegetation-index definitions (`indexes.py`). |
| **Assets / UI / i18n** | `assets/`, `ui/`, `i18n/` | Icons & logos, HTML onboarding pages, Qt translations. |

### Request flow (example: optical time series)

1. User sets an AOI and parameters in `view/optical.py`.
2. `controllers/optical_ctrl.py` collects params + AOI geometry and starts an
   `OpticalWorker` (`workers/optical_worker.py`).
3. The worker calls `OpticalService.get_time_series(...)` (`services/optical_service.py`),
   which builds the Earth Engine query through the authenticated `GEEService`.
4. On completion the worker emits `finished(data, index_name)`; the controller
   renders the chart / writes the layer via the renderers.

This keeps Earth Engine I/O on a background thread — the QGIS UI never blocks.

### Dependency provisioning

RAVI needs packages **not shipped with QGIS** (`earthengine-api`, `agrigee-lite`,
`google-*`, `cryptography`, `cffi`, …). These are ABI-locked to the Python
version, so a single bundle breaks across QGIS releases. `extlibs_manager.py`
resolves this at runtime, in order:

1. **Download a tagged prebuilt bundle** — `extlibs-<cpXY>-<platform>.zip`
   matching the running interpreter (`cp312-win_amd64`, `cp312-macosx_10_13_universal2`, …).
2. **Fallback to pip** — install `requirements.txt` into `extlibs/` using the
   QGIS Python.
3. Otherwise show manual instructions.

A `extlibs/.ready` sentinel records the active tag, so a QGIS Python upgrade
(different tag) re-provisions automatically. QGIS-provided packages
(`numpy`, `pandas`, `scipy`, `requests`, …) are deliberately **never** shadowed
from `extlibs/`.

### Build & CI

| Script / workflow | Purpose |
|---|---|
| `build_extlibs_zip.py` | Build a tagged `extlibs-*.zip` for the host (or cross-target a platform via `_PYTHON_HOST_PLATFORM`, e.g. macOS `universal2`). |
| `.github/workflows/build-extlibs.yml` | Build the full matrix (Windows / Linux / macOS × Python 3.11–3.13) and optionally commit the bundles to `main`. |
| `build_plugin.py` | Package the plugin for distribution. |
| `compile_translations.py` | Compile `i18n/` `.ts` → `.qm`. |

> Dependency versions track `requirements.txt`. `agrigee-lite` is unpinned, so a
> rebuild always pulls the latest release; bundle bytes are otherwise reproducible
> (a rebuild only changes a zip when its resolved dependency set changes).

---

## Contributing

Issues and pull requests welcome at the
[project repository](https://github.com/farmanalytica/ravi-qgis-plugin).

## License

GNU General Public License v2.0 or later. See [`LICENSE`](LICENSE).
