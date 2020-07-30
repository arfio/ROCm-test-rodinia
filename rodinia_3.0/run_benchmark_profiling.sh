#!/bin/bash

programs=("nw" "gaussian" "b+tree" "hybridsort" "backprop" "streamcluster" "kmeans" "nn" "heartwall" "dwt2d" "lud" "pathfinder" "srad" "bfs" "lavaMD" "cfd" "particlefilter" "hotspot")
rocprofiler="/opt/rocm/bin/rocprof"

perf_control_file="perf_control.txt"
perf_profiling_file="perf_profiling.txt"
perf_tracing_file="perf_tracing.txt"
perf_tracing_profiling_file="perf_tracing_profiling.txt"
files=($perf_control_file $perf_profiling_file $perf_tracing_file $perf_tracing_profiling_file)

profiling_params="-i ../../pc_config.txt --obj-tracking on"
tracing_params="--stats --hsa-trace --obj-tracking on"

n_execution=1

function run_control() {
	echo "Running control..."
	(time $exec) &>> $perf_control_file
}

function run_profiling() {
	echo "Running profiling..."
	(time $rocprofiler $profiling_params $exec) &>> $perf_profiling_file
}

function run_tracing() {
	echo "Running tracing..."
	(time $rocprofiler $tracing_params $exec) &>> $perf_tracing_file
}

function run_tracing_profiling() {
	echo "Running tracing and profiling..."
	(time $rocprofiler $tracing_params $profiling_params $exec) &>> $perf_tracing_profiling_file
	python3 ../../collect_counters.py
}

# MAIN
rm "kernel_statistics.csv"
cd "hip/nw"

for program in "${programs[@]}"; do
	cd "../${program}"
	# Deleting old results because we append results for each run
	for file in "${files[@]}"; do rm -f $file; touch $file; done
	# Defining the program to be executed
	exec="../../test/${program}/run0.cmd"
	echo -e "\033[0;32mRunning ${program}"

	# Running experiments
#	for ((i=0;i<n_execution;i++)); do run_control; done
#	for ((i=0;i<n_execution;i++)); do run_profiling; done
#	for ((i=0;i<n_execution;i++)); do run_tracing; done
	for ((i=0;i<n_execution;i++)); do run_tracing_profiling; done
done
