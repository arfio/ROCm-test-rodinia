import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


overhead_tracing_column = "Overhead w/ tracing (%)"
overhead_profiling_column = "Overhead w/ profiling (%)"
overhead_tracing_profiling_column = "Overhead w/ both (%)"

def calc(x):
    return float(x)

def get_data_from_csv():
    labels, tracing, profiling, tracing_profiling = [], [], [], []
    with open("./rodinia_3.0/result_runtime.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            labels.append(line["Experience"])
            tracing.append(calc(line[overhead_tracing_column]))
            profiling.append(calc(line[overhead_profiling_column]))
            tracing_profiling.append(calc(line[overhead_tracing_profiling_column]))
    return (labels, tracing, profiling, tracing_profiling)

(labels, tracing, profiling, tracing_profiling) = get_data_from_csv()

y = np.arange(len(labels))  # the label locations
height = 0.30  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.barh(y - height, profiling, height=height, label=overhead_profiling_column[:-4])
rects2 = ax.barh(y, tracing, height=height, label=overhead_tracing_column[:-4])
rects3 = ax.barh(y + height, tracing_profiling, height=height, label=overhead_tracing_profiling_column[:-4])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Execution Time overhead (%)')
ax.set_title('Experiments')
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        width = rect.get_width()
        ax.annotate('x{:.1f}'.format((width + 100) / 100),
                    xy=(width, rect.get_y() + rect.get_height()),
                    xytext=(15, -10.7),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()

plt.show()
