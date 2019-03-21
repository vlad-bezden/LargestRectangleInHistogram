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


if __name__ == "__main__":
    t0 = time()
    # V2 using np array
    # hists = np.array([hist for hist in histograms(10)])
    # print(f"Created {hists.shape} samples. Calc took {time() - t0:.2f} secs")

    hists = []
    areas = []
    for i, hist in enumerate(histograms(), start=1):
        if i % 1_000 == 0:
            t = time() - t0
            print(f"{i:>6,d} {t:>8.2f} Perf: {t / i * 1000:>6.2f} secs/1000 areas")
        hists.append(hist)
        areas.append(largest_rectangle_area(hist))

    print(f"Created {len(hists):,d} samples. Calc took {time() - t0:.2f} secs")

    root = Path(r".\data")
    with open(Path(root, "histograms.txt"), "w") as f:
        f.write("\n".join(map(str, hists)))

    with open(Path(root, "histograms_areas.txt"), "w") as f:
        f.write("\n".join(map(str, areas)))

    print("DONE!!!")
