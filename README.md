# fhir-test-data-generator
A generator for producing FHIR resources from either scenario based CSVs or bulk synthetic data with IG support.

## Prerequisites
Python 3

## Installation

```
pip3 install -r requirements.txt
```

## Running

Running the script will generate resources based on the selected IG, type, and mode.
Generated resources will be written to the selected IG output directory.

### Scenario mode

Scenario mode reads CSV files from the selected IG input directory and writes FHIR resources files to `output/<ig-name>/csv/`.
If `--type` is omitted, the generator scans the IG input directory and generates every supported resource that has a matching input CSV.

Examples:

`python3 generate.py --ig au-core-2.0.0 --mode scenario`

`python3 generate.py --ig au-core-2.0.0 --type observation --mode scenario`

### Bulk

Bulk mode uses Faker and writes NDJSON to `output/<ig-name>/bulk/`. It uses bounded pools so overlap stays realistic without doing full referential integrity tracking.
Bulk output is intentionally less strict than scenario mode: it aims for useful synthetic data rather than complete profile-level validity.
If `--type` is omitted, bulk mode generates all supported resource types for the selected IG.

Examples:

`python3 generate.py --ig hcpd-26.0.0 --mode bulk --count 100`

`python3 generate.py --ig au-core-2.0.0 --type patient --mode bulk --count 1000 --seed 42`

### CLI switches

`--ig`
Required. The versioned IG package to use, for example `au-core-2.0.0` or `hcpd-26.0.0`.

`--mode`
Required. The generation mode. Supported values: `scenario`, `bulk`.

`--type`
Optional. The resource type to generate. If omitted, scenario mode generates every supported type with a matching CSV in the IG input directory, and bulk mode generates every supported type for the selected IG.

`--count`
Number of resources to generate in bulk mode. Defaults to `100`.

`--seed`
Seed for deterministic random generation in bulk mode. Defaults to `42`.

Input and output directories are not configurable via CLI. The generator enforces the profile layout under `IGs/`, `input/`, and `output/`.


## Visualisation

`visualise.py` reads the generated FHIR files and produces a self-contained interactive HTML graph showing references between resources.
It accepts any directory containing `.ndjson` or `.json` files.

```sh
python visualise.py --dir output/hcpd-26.0.0/bulk
python visualise.py --dir output/au-core-2.0.0/scenario
python visualise.py --dir output/hcpd-26.0.0/bulk 
```

The graph is written to `<dir>/graph.html`.

### CLI switches

`--dir`
Required. Path to the directory containing the FHIR output files.

## Reference


### Layout

We use a profile-specific directory layout so IG assets, input data, and generated output stay aligned:

```text
IGs/<ig-name>/
input/<ig-name>/
output/<ig-name>/csv/
output/<ig-name>/bulk/
```

For Health Connect in this repo, that means:

```text
IGs/hcpd-26.0.0/
input/hcpd-26.0.0/
output/hcpd-26.0.0/csv/
output/hcpd-26.0.0/bulk/
```

The generator treats the versioned package directory as canonical and expects `IGs`, `input`, and `output` to use the same versioned name.

## Visualisation

`visualise.py` reads generated FHIR files and produces a self-contained interactive HTML graph showing references between resources.
It accepts any directory containing `.ndjson` or `.json` files. The graph is written to `graph.html` inside the same directory.

```sh
python visualise.py --dir output/hcpd-26.0.0/bulk
python visualise.py --dir output/au-core-2.0.0/scenario
```

Open the resulting `graph.html` in any browser.

### CLI switches

`--dir`
Required. Path to the directory containing the FHIR output files.

