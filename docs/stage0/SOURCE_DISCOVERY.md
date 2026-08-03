# Phase C, Step 0.7 — Current Authoritative Source Discovery

**Discovery date:** 3 August 2026  
**Tracking issue:** [#9 — Discover current authoritative sources](https://github.com/Lukeyone/geoprospect/issues/9)  
**Scope:** Source-path discovery and metadata validation only  
**Stage 1:** BLOCKED

## Result

One plausible current official pathway has been identified for every mandatory Stage 0 source class. This does not select the final Stage 1 source set, establish candidate-area coverage, prove record completeness or resolve licensing.

| Source class | Registered pathway | Publisher | Product or layer identifier | Primary access | CRS | Registry file |
|---|---|---|---|---|---|---|
| Mineral occurrences | Mines and mineral occurrence by status | State of Queensland | `7a96c3bdb2f54a0fa241a9b9e1c85bee / 12` | ArcGIS REST | Service EPSG:3857; source EPSG:7844 | `configs/sources/mineral_occurrences.yaml` |
| Detailed geology | Detailed surface geology, 1:100,000 | State of Queensland | `119775283acd4d7c82798d04d6229492 / 15` | ArcGIS REST | Service EPSG:3857; source EPSG:7844 | `configs/sources/geology.yaml` |
| Structures | Detailed faults and shear zones plus detailed folds | State of Queensland | `119775283acd4d7c82798d04d6229492 / 4, 5` | ArcGIS REST | Service EPSG:3857; source EPSG:7844 | `configs/sources/structures.yaml` |
| Magnetics | TMI RTP first vertical derivative grid, AWAGS | Geoscience Australia | `ga/144752` | NetCDF and WCS | EPSG:4283 | `configs/sources/magnetics.yaml` |
| Gravity | National Gravity Compilation 2019 CSCBA | Geoscience Australia | `geophys:Gravmap2019-grid-grv_cscba` | NetCDF; WMS for discovery/visualisation | EPSG:4283 | `configs/sources/gravity.yaml` |

The registry files use JSON syntax, which is valid YAML 1.2, so they can be validated with the Python standard library without adding an unneeded parser dependency during Stage 0.

## Underlying endpoint inspection

### Mineral occurrences

The live Queensland MiningResources ArcGIS service and layer 12 were inspected directly. The layer is point geometry, supports JSON, GeoJSON and PBF, exposes advanced-query capabilities and publishes a 2,000-record transfer limit. The schema contains source identifiers, names, commodity fields, mine and exploration status, site type, coordinates, location method, location accuracy and record dates.

The endpoint is plausible for the occurrence audit, but it is not an immutable snapshot. Step 0.9 must design count reconciliation, pagination or object-ID batching and silent-truncation controls before Step 0.10 retrieves records.

### Detailed geology

The live Queensland GeologyDetailed service and layer 15 were inspected directly. Layer 15 is the detailed surface-geology polygon layer in the detailed 1:100,000 group. It exposes unit name, map symbol, lithological summary, dominant rock, rock type and age. Layer 14 supplies a separate mapped-extent layer. Layer 17 supplies interpreted solid geology and remains a related product rather than a silent substitute for surface geology.

Detailed mapping is not assumed to cover every future candidate cell. Coverage must be measured from the mapped extent and valid polygons in Step 0.18.

### Structures

The same live GeologyDetailed service exposes faults and shear zones as layer 4 and folds as layer 5. Both are polyline layers. Their schema includes feature type or description, name, interpretation method, source and capture scale. The service legend distinguishes accurate, approximate, concealed, inferred and geophysically interpreted structures.

The two layers must remain separate and traceable. Their density, geometry validity, taxonomy completeness and regional gaps are measurements for Step 0.18.

### Magnetics

Geoscience Australia dataset `ga/144752` publishes a persistent product record and exact access paths for the national TMI RTP first-vertical-derivative grid, including NetCDF, WCS, NCSS and OPeNDAP. The grid is in GDA94, covers onshore and near-offshore Australia and has nominal cells of approximately 88 metres.

This is a reproducibly addressable candidate, not a final feature decision. The derivative enhances short-wavelength anomalies but can also amplify noise. Survey line spacing, terrain clearance, merge history and joins determine effective support; the 88-metre output cell size cannot be treated as 88-metre measurement resolution.

### Gravity

Geoscience Australia identifies the 2019 Australian National Gravity Grids as the latest published national edition. The selected candidate is the complete spherical cap Bouguer anomaly grid with layer identifier `geophys:Gravmap2019-grid-grv_cscba` and an exact NetCDF path. Its nominal cell size is approximately 435 metres in GDA94.

The grid is much finer than the effective support in areas where station spacing is several kilometres. The numeric NetCDF, rather than the WMS image, must be used for later coverage measurements. Step 0.19 must inspect nodata, survey or station context and candidate-level support.

## Freshness treatment

Catalogue modification dates are not used as proof that the underlying data are current.

- The Queensland entries rely on live service and layer metadata and retain the available per-record or feature-level update fields where present.
- The magnetic entry records its 2019 compilation period and product maintenance status.
- The gravity entry records that its source observations extend through September 2019 and that maintenance is described as as-needed.

A future source refresh or endpoint change must update the registry and repeat the relevant endpoint checks.

## Licensing boundary

Step 0.7 records licence evidence links only. It does **not** classify raw redistribution, derived-output permission, attribution wording or public-release restrictions. Every registry entry is explicitly marked `pending_step_0_8`.

The next authorised unit is **Phase C, Step 0.8 — Validate Licensing and Attribution**. Stage 1 remains blocked.
