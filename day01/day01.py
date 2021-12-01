import os.path


def count_increases(depths):
    count = 0
    for previous, current in zip(depths, depths[1:]):
        if current > previous:
            count += 1
    return count


def make_sliding_window(items, window_size=3):
    end_point = len(items) - window_size + 1
    return [sum(items[x:x+window_size]) for x in range(end_point)]


if __name__ == '__main__':
    depth_file = os.path.join(os.path.dirname(__file__), "day01_real_data.txt")
    with open(depth_file) as f:
        depths = [int(x) for x in f.readlines()]

    print("The slope increased {} times".format(count_increases(depths)))

    window_depths = make_sliding_window(depths)
    print("The slope increased {} times when using a window size of {}".format(count_increases(window_depths), "3"))
