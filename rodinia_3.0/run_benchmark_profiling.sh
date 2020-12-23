#!/bin/bash

programs=("nw" "gaussian" "b+tree" "hybridsort" "backprop" "streamcluster" "kmeans" "nn" "heartwall" "dwt2d" "lud" "pathfinder" "srad" "bfs" "lavaMD" "cfd" "particlefilter" "hotspot")
rocprofiler="/opt/rocm/bin/rocprof"
lttng="lttng"

perf_control_file="perf_control.txt"
perf_profiling_file="perf_profiling.txt"
perf_tracing_file="perf_tracing.txt"
perf_tracing_profiling_file="perf_tracing_profiling.txt"
files=($perf_control_file $perf_profiling_file $perf_tracing_file $perf_tracing_profiling_file)

lttng_params="-c k -k syscall,power_cpu_frequency,sched_process_exec,sched_process_exit,sched_process_fork,sched_process_free,sched_switch,sched_wakeup,sched_waking,sched_wakeup_new,sched_pi_setprio,irq_softirq_entry,irq_softirq_raise,irq_softirq_exit,irq_handler_entry,irq_handler_exit,net_dev_queue,net_if_receive_skb,timer_hrtimer_start,timer_hrtimer_cancel,timer_hrtimer_expire_entry,timer_hrtimer_expire_exit,timer_hrtimer_init,timer_start,timer_cancel,timer_expire_entry,timer_expire_exit,timer_init,lttng_statedump*"
profiling_params="-i ../../pc_config.txt --obj-tracking on"
tracing_params="--stats --hsa-trace --obj-tracking on"

n_execution=20

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
	$lttng create rocprof --output=./rocprof > /dev/null
	$lttng enable-channel k -k --subbuf-size 2048K --num-subbuf 8 > /dev/null
	$lttng enable-event $lttng_params > /dev/null
	$lttng start > /dev/null
	(time $rocprofiler $tracing_params $exec) &>> $perf_tracing_file
	$lttng destroy > /dev/null
}

function run_tracing_profiling() {
	echo "Running tracing and profiling..."
	$lttng create rocprof --output=./rocprof > /dev/null
	$lttng enable-channel k -k --subbuf-size 2048K --num-subbuf 8 > /dev/null
	$lttng enable-event $lttng_params > /dev/null
	$lttng start > /dev/null
	(time $rocprofiler $tracing_params $profiling_params $exec) &>> $perf_tracing_profiling_file
	$lttng destroy > /dev/null
	# Generate CTF trace
	python3 ../../../ctftrace.py results.db
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
	for ((i=0;i<n_execution;i++)); do run_control; done
	for ((i=0;i<n_execution;i++)); do run_profiling; done
	for ((i=0;i<n_execution;i++)); do run_tracing; done
	for ((i=0;i<n_execution;i++)); do run_tracing_profiling; done
done
