import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

overhead_tracing_column = "Overhead w/ tracing (%)"
overhead_profiling_column = "Overhead w/ profiling (%)"
overhead_tracing_profiling_column = "Overhead w/ both (%)"
overhead_lttng = "Overhead w/ LTTng (%)"

def calc(x):
    return float(x)

def get_data_from_csv():
    labels, tracing, profiling, tracing_profiling, lttng = [], [], [], [], []
    with open("./rodinia_3.0/result_runtime.csv", "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            labels.append(line["Experience"])
            tracing.append(calc(line[overhead_tracing_column]))
            profiling.append(calc(line[overhead_profiling_column]))
            tracing_profiling.append(calc(line[overhead_tracing_profiling_column]))
            lttng.append(calc(line[overhead_lttng]))
    return (labels, tracing, profiling, tracing_profiling, lttng)

(labels, tracing, profiling, tracing_profiling, lttng) = get_data_from_csv()

y = np.arange(len(labels))  # the label locations
height = 0.15  # the width of the bars

fig, ax = plt.subplots()

rects1 = ax.barh(y + 1.5 * height, lttng, height=height, label=overhead_lttng[:-4])
rects2 = ax.barh(y + 0.5 * height, tracing, height=height, label=overhead_tracing_column[:-4])
rects3 = ax.barh(y - 0.5 * height, profiling, height=height, label=overhead_profiling_column[:-4])
rects4 = ax.barh(y - 1.5 * height, tracing_profiling, height=height, label="Overhead w/ all")


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Execution Time overhead (%)')
ax.set_xticks(np.arange(0, 425, 25))
ax.set_title('Experiments')
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.legend()


#def autolabel(rects):
#    """Attach a text label above each bar in *rects*, displaying its height."""
#    for rect in rects:
#        width = rect.get_width()
#        ax.annotate('x{:.2f}'.format((width + 100) / 100),
#                    xy=(width, rect.get_y() + rect.get_height()),
#                    xytext=(20, -7.7),  # 3 points vertical offset
#                    textcoords="offset points",
#                    ha='center', va='bottom')


#autolabel(rects1)
#autolabel(rects2)
#autolabel(rects3)
#autolabel(rects4)

fig.tight_layout()

plt.show()
