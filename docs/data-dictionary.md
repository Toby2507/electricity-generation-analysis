## Dataset Structure

| **Dataset**     | One row represents                        | Purpose                                                   |
| --------------- | ----------------------------------------- | --------------------------------------------------------- |
| plant_monthly   | One reported plant in one reported month. | Capacity and generation performance.                      |
| plant_reference | One reported plant                        | Store attributes that helps explain differences in plants |
| grid_monthly    | One reporting month                       | Grid frequency and voltage measurements.                  |

## Variable Dictionary

| **Variable name**                   | Source label                        | Data group        | Definition                                                                                                                                 | Data type | Unit  | Observation Level | Origin          | Calculation / Derivation                        | Validation Rule         |
| ----------------------------------- | ----------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | --------- | ----- | ----------------- | --------------- | ----------------------------------------------- | ----------------------- |
| reporting_month                     | Reporting Month                     | metadata          | Month covered by the factsheet, stored as `YYYY-MM`                                                                                        | date      |       | month             | source-metadata |                                                 |                         |
| plant_name_raw                      | Plant                               | plant-metadata    | Plant name as printed in the report                                                                                                        | string    |       | plant             | source-reported |                                                 |                         |
| plant_name_standardized             |                                     | plant-metadata    | Normalized plant name                                                                                                                      | string    |       | plant             | derived         | lowercased and spaces replaced with underscores |                         |
| installed_capacity_mw               | Installed Capacity (MW)             | plant-capacity    | Maximum rated output specified by the manufacturer of a generating plant                                                                   | integer   | MW    | plant-month       | source-reported |                                                 |                         |
| average_available_capacity_mw       | Average Available Capacity (MW)     | plant-capacity    | Average available capacity of the plant declared by the operator for the month                                                             | integer   | MW    | plant-month       | source-reported |                                                 | ≤ installed_capacity_mw |
| reported_paf_pct                    | Plant Availability Factor (%)       | plant-performance | Ratio of the maximum rated output of the plant declared by the operator relative to the maximum rated output specified by the manufacturer | float     | %     | plant-month       | source-reported |                                                 | 0 ≤ x ≤ 1               |
| average_hourly_generation_mwh_per_h | Average Hourly Generation (MWh/h)   | plant-performance | Monthly average hourly generation as reported                                                                                              | integer   | MWh/h | plant-month       | source-reported |                                                 |                         |
| reported_load_factor_pct            | Load Factor (%)                     | plant-performance | Ratio of the average electricity generated over a period to the maximum possible generation                                                | float     | %     | plant-month       | source-reported |                                                 | 0 ≤ x ≤ 1               |
| avg_actual_voltage_lower_kv         | Average Actual Lower Grid Voltage   | grid-conditions   | Measured average of daily minimum voltage readings                                                                                         | float     | kV    | month             | source-reported |                                                 |                         |
| avg_actual_voltage_upper_kv         | Average Actual Upper Grid Voltage   | grid-conditions   | Measured average of daily maximum voltage readings                                                                                         | float     | kV    | month             | source-reported |                                                 |                         |
| target_voltage_lower_kv             | Target Lower Grid Voltage           | grid-conditions   | Prescribed or target minimum voltage reading from the Grid Code limits                                                                     | float     | kV    | month             | source-reported |                                                 |                         |
| target_voltage_upper_kv             | Target Upper Grid Voltage           | grid-conditions   | Prescribed or target maximum voltage reading from the Grid Code limits                                                                     | float     | kV    | month             | source-reported |                                                 |                         |
| avg_actual_frequency_lower_hz       | Average Actual Lower Grid Frequency | grid-conditions   | Measured average of daily minimum frequency readings                                                                                       | float     | Hz    | month             | source-reported |                                                 |                         |
| avg_actual_frequency_upper_hz       | Average Actual Upper Grid Frequency | grid-conditions   | Measured average of daily maximum frequency readings                                                                                       | float     | Hz    | month             | source-reported |                                                 |                         |
| target_frequency_lower_hz           | Target Lower Grid Frequency         | grid-conditions   | Prescribed or target minimum frequency reading from the Grid Code limits                                                                   | float     | Hz    | month             | source-reported |                                                 |                         |
| target_frequency_upper_hz           | Target Upper Grid Frequency         | grid-conditions   | Prescribed or target maximum frequency reading from the Grid Code limits                                                                   | float     | Hz    | month             | source-reported |                                                 |                         |
| state                               | Location                            | plant-metadata    | State of residence of plant                                                                                                                | string    |       | plant             | source-reported |                                                 |                         |
| region                              |                                     | plant-metadata    | Geographical region of plant location                                                                                                      | string    |       | plant             | derived         | Computed from the plant state                   |                         |
| ownership                           | Ownership                           | plant-metadata    | Ownership / Concessionaire classification                                                                                                  | string    |       | plant             | source-reported |                                                 |                         |
| turbine_type                        | Turbine Type                        | plant-metadata    | Turbine technology category                                                                                                                | string    |       | plant             | source-reported |                                                 |                         |
| fuel_type                           | Fuel Type                           | plant-metadata    | Fuel Category                                                                                                                              | string    |       | plant             | source-reported |                                                 |                         |

## NERC Abbreviations

| Abbreviations | Full Names                                 | Notes                                   |
| ------------- | ------------------------------------------ | --------------------------------------- |
| NERC          | Nigerian Electricity Regulatory Commission | Regulators                              |
| NBET          | Nigerian Bulk Electricity Trading Plc.     | Bulk power traders (wholesale market)   |
| GenCos        | Generation Companies                       | Upstream (power plants)                 |
| DisCos        | Distribution Companies                     | Downstream                              |
| NIPP          | National Integrated Power Project          | Government-owner plants                 |
| NESI          | Nigerian Electricity Supply Industry       | The entire sector                       |
| PHCN          | Power Holding Company of Nigeria           | Pre-2013 privatisation                  |
| PPA           | Power Purchase Agreement                   | Contract between GenCos and DisCos/NBET |

### Ownership Types

| Category   | Meaning                                                                                                                                                                            |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NIPP       | Owned by the **Niger Delta Power Holding Company (NDPHC)**, which is jointly owned by the three tiers of government (federal, state, and local)                                    |
| IPP        | Independent Power Producers. If established before 2013 sector reform, operates under a PPA with NBET, otherwise, they operate with a sovereign-backed PPA or a bilateral contract |
| Privatised | Formerly government-owned (PHCN) plants that were privatised under the 2013 reform programme                                                                                       |
| Concession | Operator holds a concession agreement over a government-owned plant (e.g. NIPP plants)                                                                                             |

### Turbine Types

| Type                       | Abbreviation | Description                                                                                                                     |
| -------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| Hydro                      | HT           | Water-driven turbine (run-of-river or reservoir)                                                                                |
| Open Cycle Gas Turbine     | OC           | Simple-cycle gas turbine; exhaust vented to atmosphere. Thermal efficiency ~30–35%                                              |
| Combined Cycle Gas Turbine | CC           | Gas turbine + heat-recovery steam generator + steam turbine. Thermal efficiency ~55–60%                                         |
| Gas/Steam                  | GS           | Hybrid configuration; gas turbine and steam turbine at the same site but not in a true combined-cycle heat-recovery arrangement |

## Plant Reference Data and Provenance

### Source

Plant-level contextual attributes were obtained from the Nigerian Electricity Regulatory Commission (NERC) annual reports for 2024 and 2025.

### Attributes

The reference dataset contains plant names, locations, ownership classifications, turbine types, and fuel types. Geographic regions are derived from the reported state of location.

### Standardization and Verification

Plant names were standardized to support consistent identification and joining with the monthly operational performance dataset. Attribute values were compared across the 2024 and 2025 annual reports. No differences were identified in the ownership, turbine type, or fuel type of the plants compared.

Each distinct plant is therefore represented by a single reference record for the scope of this analysis.

### Limitations

The reference attributes represent the information reported in the annual reports reviewed. Their consistency across the two reports does not establish that these attributes remained unchanged outside the period or sources examined. Derived geographic classifications and any unresolved plant-name mappings should be documented separately.
