import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        offset = -11 if rect.get_height() < 0 else 0
        ax.annotate('{:.2f}'.format(height),
                    xy=(rect.get_x() + rect.get_width(), height),
                    xytext=(-5, offset),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

def plot_data(df, experiment_name):
    x = np.arange(len(df))  # the label locations
    width = 0.30  # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(x, df, width=width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Correlation coefficient')
    ax.set_title('Correlation between {} overhead and performance metrics'.format(experiment_name))
    ax.set_xticks(x)
    ax.set_xticklabels(df.index, rotation=45)
    autolabel(rects, ax)
    fig.set_size_inches(7, 6, forward=True)
    fig.tight_layout()
    plt.show()


kernel_stats = pd.read_csv("./rodinia_3.0/kernel_statistics.csv", delimiter=',')
runtime_stats = pd.read_csv("./rodinia_3.0/result_runtime.csv")

kernel_stats["DurationNs"] = kernel_stats["DurationNs"] / kernel_stats["NKernels"]
kernel_stats["L2CacheHit"] = kernel_stats["L2CacheHit"] / kernel_stats["NKernels"]
kernel_stats["VALUInsts"] = kernel_stats["VALUInsts"] / kernel_stats["NKernels"]
kernel_stats["SALUInsts"] = kernel_stats["SALUInsts"] / kernel_stats["NKernels"]
kernel_stats["FlatVMemInsts"] = kernel_stats["FlatVMemInsts"] / kernel_stats["NKernels"]
kernel_stats["LDSInsts"] = kernel_stats["LDSInsts"] / kernel_stats["NKernels"]
kernel_stats["GDSInsts"] = kernel_stats["GDSInsts"] / kernel_stats["NKernels"]
kernel_stats["Wavefronts"] = kernel_stats["Wavefronts"] / kernel_stats["NKernels"]

kernel_stats["VALUInsts"] = kernel_stats["VALUInsts"] / kernel_stats["DurationNs"]
kernel_stats["SALUInsts"] = kernel_stats["SALUInsts"] / kernel_stats["DurationNs"]
kernel_stats["FlatVMemInsts"] = kernel_stats["FlatVMemInsts"] / kernel_stats["DurationNs"]
kernel_stats["LDSInsts"] = kernel_stats["LDSInsts"] / kernel_stats["DurationNs"]
kernel_stats["GDSInsts"] = kernel_stats["GDSInsts"] / kernel_stats["DurationNs"]

tracing_column = "Overhead w/ tracing (%)"
profiling_column = "Overhead w/ profiling (%)"
tracing_profiling_column = "Overhead w/ both (%)"

stats = pd.merge(kernel_stats, runtime_stats, on="Experience")
stats.drop(columns=["GDSInsts"], inplace=True)

corr = stats.corr(method="pearson")

irrelevant_metrics = [tracing_column, profiling_column, tracing_profiling_column,
    "Control (s)", "Profiling (s)", "Tracing (s)", "Tracing and profiling (s)",
    "Control std", "Profiling std", "Tracing std", "Tracing and profiling std"]

corr_tracing = corr.sort_values(by=[tracing_column])[tracing_column]
corr_tracing.drop(index=irrelevant_metrics, inplace=True)
corr_profiling = corr.sort_values(by=[profiling_column])[profiling_column]
corr_profiling.drop(index=irrelevant_metrics, inplace=True)
corr_tracing_profiling = corr.sort_values(by=[tracing_profiling_column])[tracing_profiling_column]
corr_tracing_profiling.drop(index=irrelevant_metrics, inplace=True)

plot_data(corr_tracing, "tracing")
plot_data(corr_profiling, "profiling")
plot_data(corr_tracing_profiling, "tracing and profiling")
