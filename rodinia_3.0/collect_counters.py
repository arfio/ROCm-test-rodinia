import csv
import json
import os
import sys
from datetime import datetime

perf_counters = {
    "Wavefronts": 0,
    "L2CacheHit": 0,
    "VALUInsts": 0,
    "SALUInsts": 0,
    "FlatVMemInsts": 0,
    "LDSInsts": 0,
    "GDSInsts": 0,
    "DurationNs": 0,
    "NKernels": 0
}

def read_source_csv(filename):
    with open(filename) as kernel_table_file:
        csv_reader = csv.DictReader(kernel_table_file, delimiter=',')
        for line in csv_reader:
            for counter in perf_counters:
                if counter == "NKernels":
                    perf_counters[counter] += 1
                else:
                    perf_counters[counter] += int(line[counter])
    return perf_counters


def get_event_count(trace_filename):
    with open(trace_filename) as trace_file:
        return len(json.load(trace_file)["traceEvents"])

def get_trace_size(trace_folder):
    return sum(os.path.getsize(os.path.join(trace_folder, f)) for f in os.listdir("./{}".format(trace_folder)))


filename_stats = "pc_config.csv"
trace_filename = "pc_config.json"
kernel_stats = "../../kernel_statistics.csv"
performance_counters = read_source_csv(filename_stats)
performance_counters["NEvents"] = get_event_count(trace_filename)

rocm_trace_folder = "results"
lttng_trace_folder = "rocprof"

performance_counters["TraceSize"] = get_trace_size(rocm_trace_folder) + get_trace_size(lttng_trace_folder)

experience_name = os.path.basename(os.getcwd())
performance_counters["Experience"] = experience_name

file_exists = os.path.isfile(kernel_stats)
with open(kernel_stats, 'a') as statistics:
    writer = csv.DictWriter(statistics, fieldnames=performance_counters.keys())
    if not file_exists:
        writer.writeheader()

    writer.writerow(performance_counters)



