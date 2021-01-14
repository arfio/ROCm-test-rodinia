import csv
import re
import json
from os import path
from math import sqrt

programs = ["nw","gaussian","b+tree","hybridsort","backprop","streamcluster","kmeans","nn","heartwall","dwt2d","lud","pathfinder","srad","bfs","lavaMD","cfd","particlefilter","hotspot"]
files = ["perf_control.txt","perf_profiling.txt","perf_tracing.txt","perf_tracing_profiling.txt", "perf_lttng.txt"]

stat_regex = re.compile("real\t(\d+m\d+[.]\d+)s\nuser\t(\d+m\d+[.]\d+)s\nsys\t(\d+m\d+[.]\d+)s")
result_filename = "result_statistics.json"
result_csv = "result_runtime.csv"

def extract_statistics(filename):
    with open(filename, "r") as text_file:
        data = text_file.read()
        results = re.findall(stat_regex, data)
        return {
            "real": [int(match[0].split("m")[0])*60 + float(match[0].split("m")[1]) for match in results],
            "user": [int(match[1].split("m")[0])*60 + float(match[1].split("m")[1]) for match in results],
            "sys": [int(match[2].split("m")[0])*60 + float(match[2].split("m")[1]) for match in results]
        }
        

def calculate_average(statistics):
    average_statistics = {}
    for program in statistics:
        average_statistics[program] = {}
        for experience in statistics[program]:
            timings = statistics[program][experience]
            real_average = round(sum(timings["real"]) / len(timings["real"]), 4)
            average_statistics[program][experience] = {
                "real": real_average,
                "real_std": round(sqrt(sum((x-real_average)**2 for x in timings["real"]) / len(timings["real"])), 6),
                "user": round(sum(timings["user"]) / len(timings["user"]), 4),
                "sys": round(sum(timings["sys"]) / len(timings["sys"]), 4)
            }
    return average_statistics

def overhead_rate(indirect, baseline):
    return round(((indirect / baseline) - 1) * 100, 3)

def calculate_overhead(average_statistics):
    overhead = {}
    for program in average_statistics:
        overhead[program] = {}
        baseline = average_statistics[program]["control"]["real"]
        overhead[program]["profiling"] = overhead_rate(average_statistics[program]["profiling"]["real"], baseline)
        overhead[program]["tracing"] = overhead_rate(average_statistics[program]["tracing"]["real"], baseline)
        overhead[program]["tracing_profiling"] = overhead_rate(average_statistics[program]["tracing_profiling"]["real"], baseline)
        overhead[program]["lttng"] = overhead_rate(average_statistics[program]["lttng"]["real"], baseline)

    n_prog = len(programs)
    overall = {}
    overall["profiling"] = sum([x["profiling"] for x in overhead.values()]) / n_prog
    overall["tracing"] = sum([x["tracing"] for x in overhead.values()]) / n_prog
    overall["tracing_profiling"] = sum([x["tracing_profiling"] for x in overhead.values()]) / n_prog
    overall["lttng"] = sum([x["lttng"] for x in overhead.values()]) / n_prog
    overhead["overall"] = overall
    return overhead

def save_to_csv(stats, overhead):
    fieldnames = [
        "Experience",
        "Control (s)",
        "Control std",
        "Tracing (s)",
        "Tracing std",
        "Profiling (s)",
        "Profiling std",
        "Tracing and profiling (s)",
        "Tracing and profiling std",
        "LTTng (s)",
        "LTTng std",
        "Overhead w/ tracing (%)",
        "Overhead w/ profiling (%)",
        "Overhead w/ LTTng (%)",
        "Overhead w/ both (%)"
    ]
    with open(result_csv, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for experience in stats:
            writer.writerow({
                "Experience": experience,
                "Control (s)": stats[experience]["control"]["real"],
                "Control std": stats[experience]["control"]["real_std"],
                "Tracing (s)": stats[experience]["tracing"]["real"],
                "Tracing std": stats[experience]["tracing"]["real_std"],
                "Profiling (s)": stats[experience]["profiling"]["real"],
                "Profiling std": stats[experience]["profiling"]["real_std"],
                "Tracing and profiling (s)": stats[experience]["tracing_profiling"]["real"],
                "Tracing and profiling std": stats[experience]["tracing_profiling"]["real_std"],
                "LTTng (s)": stats[experience]["lttng"]["real"],
                "LTTng std": stats[experience]["lttng"]["real_std"],
                "Overhead w/ tracing (%)": overhead[experience]["tracing"],
                "Overhead w/ profiling (%)": overhead[experience]["profiling"],
                "Overhead w/ LTTng (%)": overhead[experience]["lttng"],
                "Overhead w/ both (%)": overhead[experience]["tracing_profiling"]
            })


if __name__ == "__main__":
    # Going through every program performance report
    statistics = {}
    for program in programs:
        statistics[program] = {}
        for perf_file in files:
            file_path = path.join("./hip/", program, perf_file)
            statistics[program][perf_file[5:-4]] = extract_statistics(file_path)
    # Writing all the results to a json
    with open(result_filename, "w+") as result_file:
        json.dump(statistics, result_file, indent=4)
    average_statistics = calculate_average(statistics)
    overhead = calculate_overhead(average_statistics)
    save_to_csv(average_statistics, overhead)

