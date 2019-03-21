from random import randrange, sample
from time import time
import numpy as np
from pathlib import Path


# number of samples
SAMPLES = 1_000_000
# max width and height of one histogram. X buckets each X height
MAX_HIST_SIZE = 100


def largest_rectangle_area(hist):
    max_area = 0
    hist = [-1] + hist
    hist.append(-1)
    n = len(hist)
    stack = [0]  # store index

    for i in range(n):
        while hist[i] < hist[stack[-1]]:
            h = hist[stack.pop()]
            area = h * (i - stack[-1] - 1)
            max_area = max(max_area, area)
        stack.append(i)
    return max_area


# Create historgram
def histograms(samples=SAMPLES):
    for _ in range(samples):
        yield sample(range(MAX_HIST_SIZE), randrange(MAX_HIST_SIZE))


def save_data(data, file):
    path = Path(r".\data", file)
    np.save(path, data)


def generate_data():
    hists = []
    areas = np.array([], int)
    t0 = time()
    for i, hist in enumerate(histograms(), start=1):
        if i % 1_000 == 0:
            t = time() - t0
            print(f"{i:>6,d} {t:>8.2f} Perf: {t / i * 1000:>6.2f} secs/1000 areas")
        hists.append(np.array(hist))
        areas = np.append(areas, largest_rectangle_area(hist))
    return hists, areas


def main():
    t0 = time()
    hists, areas = generate_data()
    print(f"Created {len(hists):,d} samples. Calc took {time() - t0:.2f} secs")

    t0 = time()
    save_data(hists, "histograms")
    save_data(areas, "histograms_areas")
    print(f"Saving data to disk took {time() - t0:.2f} secs")


if __name__ == "__main__":
    main()
    print("DONE!!!")
