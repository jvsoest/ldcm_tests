# LinkedDicom Performance Testing Suite

This repository contains a comprehensive testing suite for evaluating the performance of different RDF storage and querying approaches for LinkedDicom medical imaging data.

## Overview

The test suite compares two main approaches for handling LinkedDicom RDF data:
1. **RDF4J**: A Java-based triple store running in Docker
2. **RDFLib**: A Python-based in-memory RDF library with two loading strategies:
   - Per-patient loading and querying
   - Batch loading of multiple patients

## Prerequisites

- Python 3.x
- Docker
- Required Python packages (see `requirements.txt`):
  ```
  xnat
  pydicom<3.0
  LinkedDicom
  rdflib
  pandas
  scikit-learn
  numpy
  matplotlib
  ```

## Installation

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Data Preparation

### Downloading Source Data

The test data is downloaded from an XNAT server using [`download.py`](download.py):

```bash
python download.py
```

**What it does:**
- Connects to XNAT server at [`https://xnat.health-ri.nl`](https://xnat.health-ri.nl)
- Accesses the `stwstrategyhn1` project
- Downloads all scans for each subject and experiment
- Organizes data into the directory structure: `./data/{subject}/{experiment}/{scan}`
- Automatically extracts ZIP files and removes archives

**Note:** You need valid credentials for the XNAT server. The script will prompt for authentication.

### Converting to LinkedDicom

After downloading the DICOM files, convert them to LinkedDicom TTL format using [`process.py`](process.py):

```bash
python process.py
```

**What it does:**
- Uses the LinkedDicom library to process DICOM files
- Processes each patient folder sequentially
- Converts DICOM metadata to RDF triples using the [`LinkedDicom.owl`](LinkedDicom.owl) ontology
- Saves results as `LinkedDicom.ttl` in each patient directory
- Records processing times in [`data_processing_times.csv`](data_processing_times.csv)

### Analyzing Triple Counts

To analyze the generated TTL files and collect statistics:

```bash
python explorer.triples.py
```

**What it does:**
- Scans all `LinkedDicom.ttl` files in the data directory
- Counts the number of triples in each file
- Measures file sizes in KB
- Generates [`data_triples_analysis.csv`](data_triples_analysis.csv) with statistics for correlation analysis

## Data Structure

The test suite expects data in the following structure:
```
data/
├── HN1004/
│   ├── LinkedDicom.ttl
│   └── HN1004_20190403_CT/
├── HN1006/
│   ├── LinkedDicom.ttl
│   ├── HN1006_20190404_CT/
│   └── HN1006_20190404_PET/
└── [additional patient directories...]
```

Each patient directory contains:
- `LinkedDicom.ttl`: RDF representation of DICOM metadata
- Subdirectories with imaging series data

## Test Suite Components

### 1. RDF4J Tests ([`test_rdf4j.py`](test_rdf4j.py))

Tests the performance of RDF4J triple store for loading and querying LinkedDicom data.

**Process:**
- Creates a native RDF4J repository with optimized triple indexes (`spoc,posc,cspo`)
- Loads all patient TTL files into the repository
- Executes a complex SPARQL query linking RT structures with CT series
- Outputs results to [`data_analysis_results_rdf4j.csv`](data_analysis_results_rdf4j.csv)

**Key Functions:**
- `create_repository()`: Sets up RDF4J repository using PUT request with Turtle configuration
- `load_data()`: Bulk loads all TTL files via HTTP POST with `text/turtle` content type
- `run_query()`: Executes SPARQL query and returns JSON results

### 2. RDFLib Per-Patient Tests ([`analyse.py`](analyse.py))

Tests the performance of loading and querying each patient's data independently.

**Process:**
- Iterates through each patient directory
- Creates a new RDFLib graph per patient
- Loads the patient's TTL file
- Executes the SPARQL query
- Measures elapsed time per patient

**Outputs:**
- [`data_analysis_times.csv`](data_analysis_times.csv): Per-patient loading and querying times
- [`data_analysis_results.csv`](data_analysis_results.csv): Aggregated query results

### 3. RDFLib Batch Loading Tests ([`analyse_once.py`](analyse_once.py))

Tests the performance of loading multiple patients into a single RDF graph before querying.

**Process:**
- Creates a single RDFLib graph
- Loads N patients' TTL files sequentially into the same graph
- Executes a single SPARQL query on the combined dataset
- Measures loading time, query time, and result serialization time

**Usage:**
```bash
python analyse_once.py [num_patients]
```

**Outputs:**
- [`data_analysis_results_once.csv`](data_analysis_results_once.csv): Query results for batch-loaded data
- Console output with timing breakdowns

### 5. SPARQL Queries

**[`query.sparql`](query.sparql)** - Main query for linking RT structures with CT series

Links radiotherapy structure sets with CT imaging series:
- Finds all patients with RT structure data
- Links RT structures to their referenced CT series
- Retrieves structure names and CT series metadata (modality, description, manufacturer)
- Complex joins across patient → study → series → images with nested sequence items

## Running the Test Suite

### Full Test Suite

Run all tests sequentially:
```bash
bash run_tests.sh
```

See [`run_tests.sh`](run_tests.sh) for details.

This script executes:
1. RDF4J test (all patients)
2. RDFLib per-patient test (all patients)
3. RDFLib batch loading tests (1, 2, and 3 patients)

Each test is wrapped with `/usr/bin/time -v` to capture detailed resource usage metrics.

### Individual Tests

**RDF4J Test:**
```bash
bash run_rdf4j.sh  # Start Docker container
python test_rdf4j.py
```

See [`run_rdf4j.sh`](run_rdf4j.sh) for Docker configuration.

**RDFLib Per-Patient:**
```bash
python analyse.py
```

**RDFLib Batch Loading:**
```bash
python analyse_once.py 5  # Load 5 patients
```

## Statistical Analysis

### Running the Analysis

```bash
python statistical_analysis.py
```

### Analysis Components

The statistical analysis script ([`statistical_analysis.py`](statistical_analysis.py)) performs correlation analysis between:

1. **Number of Triples vs File Size**
   - Correlation coefficient calculation
   - Scatter plot: [`file_size_vs_number_of_triples.png`](file_size_vs_number_of_triples.png)

2. **Number of Triples vs Processing Time**
   - Correlation between graph size and query execution time
   - Scatter plot: [`elapsed_time_vs_number_of_triples.png`](elapsed_time_vs_number_of_triples.png)

3. **File Size vs Processing Time**
   - Correlation between file size and elapsed time
   - Scatter plot: [`elapsed_time_vs_file_size.png`](elapsed_time_vs_file_size.png)

### Data Preparation

The analysis:
- Merges [`data_analysis_times.csv`](data_analysis_times.csv) with [`data_triples_analysis.csv`](data_triples_analysis.csv)
- Cleans data by removing:
  - Rows with negative elapsed times
  - Rows with zero triples
- Calculates Pearson correlation coefficients
- Generates visualization plots

### Expected Results

**Typical Findings:**
- **Strong positive correlation** between number of triples and file size (r > 0.9)
  - More triples = larger files (linear relationship)
  
- **Moderate to strong positive correlation** between number of triples and processing time
  - Larger graphs take longer to query
  - Correlation strength varies by query complexity
  
- **Positive correlation** between file size and processing time
  - Larger files take longer to parse and load

### Interpreting Correlation Values

- **r > 0.7**: Strong positive correlation
- **0.4 < r < 0.7**: Moderate positive correlation
- **r < 0.4**: Weak correlation

## Output Files

| File | Description |
|------|-------------|
| [`data_analysis_results_rdf4j.csv`](data_analysis_results_rdf4j.csv) | Query results from RDF4J test |
| [`data_analysis_results.csv`](data_analysis_results.csv) | Query results from per-patient RDFLib test |
| [`data_analysis_results_once.csv`](data_analysis_results_once.csv) | Query results from batch RDFLib test |
| [`data_analysis_times.csv`](data_analysis_times.csv) | Per-patient processing times |
| [`data_processing_times.csv`](data_processing_times.csv) | DICOM to TTL conversion times |
| [`data_triples_analysis.csv`](data_triples_analysis.csv) | Triple counts and file sizes per patient |
| [`file_size_vs_number_of_triples.png`](file_size_vs_number_of_triples.png) | Correlation plot (generated by statistical_analysis.py) |
| [`elapsed_time_vs_number_of_triples.png`](elapsed_time_vs_number_of_triples.png) | Performance correlation plot (generated by statistical_analysis.py) |
| [`elapsed_time_vs_file_size.png`](elapsed_time_vs_file_size.png) | Size/time correlation plot (generated by statistical_analysis.py) |
| [`processing_times.txt`](processing_times.txt) | Additional timing data |
| [`results.txt`](results.txt) | Additional query results |

## Performance Considerations

### RDF4J Optimization
- Uses native store for better performance
- Optimized triple indexes: `spoc,posc,cspo`
- Runs with 8GB heap size (`-Xmx8g`)
- Persistent storage via Docker volume

### RDFLib Optimization
- **Per-patient approach**: Lower memory footprint, but higher overhead per query
- **Batch approach**: Single graph in memory, faster querying but higher memory usage
- Query result iteration should be done once (materialize to list if needed multiple times)

### Known Issues

1. **Iterator Exhaustion**: SPARQL results are iterators that can only be traversed once
   - **Solution**: Convert to list: `results_list = list(results)`

2. **RDF4J Content-Type**: Must use `text/turtle` (not `application/x-turtle`)

3. **Repository Creation**: RDF4J requires PUT requests with Turtle config (not POST with JSON)

## Docker Management

**Start RDF4J:**
```bash
bash run_rdf4j.sh
```

**Stop RDF4J:**
```bash
docker stop rdf4j
docker volume rm rdf4j-data
```

## Future Improvements

- Add support for parallel patient processing
- Compare with additional triple stores (Virtuoso, Blazegraph, etc.)
- compare with javascript or java libraries
- Optimize SPARQL query patterns
