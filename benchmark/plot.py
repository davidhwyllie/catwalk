"""Create plots based on data generated by bench.py."""

import json
import statistics
import sys

import argh
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats
import plotille


def go(filename):
    """Main function."""
    data = json.loads(open(filename).read())
    distance_times = data["distance_times"]
    sample_counts = data["sample_counts"]
    distances = distance_times.keys()
    averages = [statistics.mean(row.values()) for row in distance_times.values()]

    fig = plt.gcf()
    ax1 = fig.add_subplot(111)

    # plot 1
    # show the average comparison time for a sample against all samples for given
    # distances

    errors = [scipy.stats.sem(list(row.values())) for row in distance_times.values()]
    plt.xlabel("SNP Distance")
    plt.ylabel("Seconds")

    ax1.errorbar(
        distances,
        averages,
        errors,
        elinewidth=1,
        capsize=0,
        color="r",
        label="Average time taken for comparison",
    )

    fig.set_size_inches(13, 9)
    plt.title(f"Performance for dataset {sys.argv[1]}")
    ax1.set_xticks(ax1.get_xticks()[::5])
    plt.savefig(f"{filename}-times.png")
    plt.close()

    # plot 2
    # take the N samples above, sort by number of unknown positions, divide sorted
    # list into quarters and plot average comparison time against distance format
    # the four sets of samples

    sorted_by_unknown_positions = sorted(
        [
            {"sample_name": k, "unknown_positions": v["N"]}
            for k, v in sample_counts.items()
        ],
        key=lambda x: x["unknown_positions"],
    )

    dataS = np.array_split(sorted_by_unknown_positions, 4)
    linestyles = ["solid", "dotted", "dashed", "dashdot"]
    colors = ["blue", "red", "black", "cyan"]
    print(dataS)

    ax1 = plt.gca()
    fig = plt.gcf()

    for i, data in enumerate(dataS):
        xs = distances
        ys = list()
        errs = list()
        for distance in distances:
            vs = list()
            for v in data:
                sample_name = v["sample_name"]
                distance_time = distance_times[distance][sample_name]
                vs.append(distance_time)
            ys.append(statistics.mean(vs))
            errs.append(scipy.stats.sem(vs))
        print(ys)
        ax1.plot(
            xs,
            ys,
            color=colors[i],
            linestyle=linestyles[i],
            label=f"{i*25}%-{(i+1)*25}%",
        )

    fig.set_size_inches(13, 9)
    plt.xlabel("Comparison distance")
    plt.ylabel("Time [s]")
    ax1.legend()
    plt.title(f"Comparison time for # of unknown positions\n(dataset {sys.argv[1]})")
    ax1.set_xticks(ax1.get_xticks()[::5])
    plt.savefig(f"{filename}-unknownpos.png")
    plt.close()

    # plot 3
    # take the N samples above, sort by distance from reference, divide sorted
    # list into quarters and plot average comparison time against distance format
    # the four sets of samples

    sorted_by_unknown_positions = sorted(
        [
            {"sample_name": k, "refdist": v["A"] + v["C"] + v["G"] + v["T"]}
            for k, v in sample_counts.items()
        ],
        key=lambda x: x["refdist"],
    )

    dataS = np.array_split(sorted_by_unknown_positions, 4)

    ax1 = plt.gca()
    fig = plt.gcf()

    for i, data in enumerate(dataS):
        xs = distances
        ys = list()
        errs = list()
        for distance in distances:
            vs = list()
            for v in data:
                sample_name = v["sample_name"]
                distance_time = distance_times[distance][sample_name]
                vs.append(distance_time)
            ys.append(statistics.mean(vs))
            errs.append(scipy.stats.sem(vs))
        print(ys)
        ax1.plot(
            xs,
            ys,
            color=colors[i],
            linestyle=linestyles[i],
            label=f"{i*25}%-{(i+1)*25}%",
        )

    fig.set_size_inches(13, 9)
    plt.xlabel("Comparison distance")
    plt.ylabel("Time [s]")
    ax1.legend()
    plt.title(f"Comparison time by distance from reference\n(dataset {sys.argv[1]})")
    ax1.set_xticks(ax1.get_xticks()[::5])
    plt.savefig(f"{filename}-refdist.png")
    plt.close()


if __name__ == "__main__":
    argh.dispatch_command(go)
