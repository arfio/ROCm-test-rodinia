# ROCm-test-rodinia

## Requirements
To run the experiments:
- ROCm installed ([How to install ROCm](https://rocmdocs.amd.com/en/latest/Installation_Guide/Installation-Guide.html))
- ROC-tracer `sudo apt-get install roctracer-dev`
- ROC-profiler `sudo apt-get install rocprofiler-dev`
- Python 3.x

To generate the visualizations:
- Python 3.x
- Pandas
- Matplotlib
- Numpy

## Instructions

These commands will build the Rodinia files and run the benchmark.
To modify the number of times each experiment is run, you must modify the "n_execution" parameter inside the run_benchmark_profiling.sh script.
```
cd ROCm-test-rodinia/rodinia_3.0/hip
make
cd ..
./run_benchmark_profiling.sh
python3 collect_stats.py
```

To generate the visualizations:
```
cd ../
python3 display_runtime_overhead.py
python3 analyze_correlation.py
```
