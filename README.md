## General Structure
- `tools` consists of an evaluation tool for performance of realisability and consistency analysis 
- `data` consists of necessary data files for the tools:
    - annotated feature model of the BCS case study (`model.xml`, `model.dimacs`)
    - resource type definitions (`resource_types.csv`)
    - resource provisionings (`resource_provisionings.csv`)
- `results` consists of the result data of the performance evaluation for deciding the conistency of the BCS case study (`timings_20240416.csv`)

## Re-Run Performance Evaluation
1. Start terminal in the directory `tools`.
2. Start performance analysis with `python3 ./main.py 1000` (`1000` is a command line parameter to define the number of runs the evaluation will do)
3. After the execution ends, a file `timings.csv` is written to the directory `results` comprising all information.

## Timings-File
Results of a performance evaluation are written to a file `timings.csv`. It consists of the following information per row:
- seed used in the solver for generating configuration sequences
- number of configurations visited until consistency-breaking configuration found
- total run-time
- accumulated run-time for computing validity of configurations
- accumulated run-time for computing realisability of configurations

## Affiliation
Paper Submission "Consistency Is Key: Can Your Product Line Realise What It Models?"
