## Source Overview

- **Source organisation:** Nigerian Electricity Regulatory Commission (NERC)
- **Source type:** Monthly operational performance factsheet in PDF format
- **Subject:** Operational performance of grid-connected power plants and reported grid conditions
- **Expected reporting period:** January 2024 - August 2026
- **Primary source format:** PDF; reports inspected so far appear to contain scanned pages
- **Intended use:** Construct a standardized dataset for longitudinal analysis of reported generation performance

## Source Inventory

The machine-readable inventory is maintained in `data/metadata/source-manifest.csv` .

Each available PDF should be recorded individually. Reporting periods for which no PDF has been located should also be recorded so that coverage gaps are explicit.

## Reporting Coverage

- **January 2024 – April 2026:** 28 months listed as complete in the current inventory; verification of the full contents is still pending.
- **May – July 2026:** Reports not located; availability remains unconfirmed.
- **August 2026:** Report located; plant data partial, grid data complete, according to the current inventory.
- **August – December 2025:** Two files per month, with plant and grid sections split across the files.

## Extraction Considerations

The reports appears to require OCR and table reconstruction. Extraction methods will be evaluated on a small sample before processing the full collection.

## Completeness Criteria

A report is considered complete for the intended analysis only when:

1. Its reporting month is identifiable.
2. The plant-level table and required variables are present and legible.
3. The required grid-condition measurements are present and legible, if those measurements are in scope.
4. The extracted values can be checked against the original document.

A report may be usable for some analyses but incomplete for others.

## Source Limitations and Decisions

Document reporting gaps, changes in table structure, changes in variable definitions, illegible values and decisions about whether particular reports or sections can be used.

Do not treat missing reports, missing plant records and explicitly reported zero values as equivalent.
