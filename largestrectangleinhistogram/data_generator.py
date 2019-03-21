"""
Generates list of histograms (2D numpy array) and list of areas for each histogram
"""
from random import randrange, sample
from time import time
import numpy as np
from pathlib import Path


# number of samples
SAMPLES = 100_000
# max width and height of one histogram. X buckets each X height
MAX_HIST_SIZE = 100
# data root directory
DATA_ROOT_DIR = r".\data"


def largest_rectangle_area(hist):
    """Calculates area for histogram."""
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
    """Generates histogram. Histogram is an 1D array of buckets."""
    for _ in range(samples):
        yield sample(range(MAX_HIST_SIZE), randrange(MAX_HIST_SIZE))


def save_data(data, file):
    """
    Saves data to numpy binary format.
    Using np.savetxt is about 50-100 times slower, but it's about 1.5 - 2 times less
    files size. np.save is much-much faster (less than a second). np.save is also
    stores data in binary format, so it can't be read.

    np.savetxt(path, data, fmt="%s")
    """
    path = Path(DATA_ROOT_DIR, file)
    np.save(path, data)


def generate_data():
    """Creates histograms (2D array) and 1D array of answers."""
    hists = []
    areas = np.array([], int)
    t0 = time()
    for i, hist in enumerate(histograms(), start=1):
        if i % 1_000 == 0:
            t = time() - t0
            print(f"{i:>8,d} {t:>8.2f}  {t / i * 1000:>6.2f} secs/1K areas")
        hists.append(np.array(hist))
        areas = np.append(areas, largest_rectangle_area(hist))
    return hists, areas


def main():
    """Main driver of the application."""
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
