import os


def load_instructions(filename):
    instructions_file = os.path.join(os.path.dirname(__file__), filename)
    dots = []
    folds = []
    with open(instructions_file) as f:
        for line in f.readlines():
            line = line.strip()  # wish that readlines got rid of newlines
            if not line:
                continue
            if line.startswith('fold'):
                "fold along x=<>"
                axis, position = line.split('=')
                folds.append((axis[-1], int(position)))
            else:
                x, y = line.split(',')
                dots.append((int(x), int(y)))
    return dots, folds


def make_dot_array(dots):
    width = max(x + 1 for x, y in dots)
    height = max(y + 1 for x, y in dots)
    result = [["."] * width for _ in range(height)]
    for x, y in dots:
        result[y][x] = "#"
    return result


def draw_dots(dot_array):
    result = ""
    for row in dot_array:
        result += ''.join(row)
        result += '\n'
    return result


def fold(array, axis, fold_position):
    if axis == "y":
        folded_array = do_horizontal_fold(array, fold_position)
    elif axis == "x":
        rotated_array = [list(column) for column in zip(*array)]
        folded_array = do_horizontal_fold(rotated_array, fold_position)
        folded_array = [list(column) for column in zip(*folded_array)]
    else:
        ValueError("Unknown axis: {}".format(axis))
    return folded_array


def do_horizontal_fold(array, fold_position):
    folded_array = []
    # folded_array = [row for row_index, row in enumerate(array) if row_index < fold_position]
    for original_row, folded_row in zip(array[:fold_position], array[-1: fold_position: -1]):
        row = ['#' if (c1 == '#' or c2 == '#') else '.' for c1, c2 in zip(original_row, folded_row)]
        folded_array.append(row)
    return folded_array


def count_dots(array):
    return sum(c == '#' for row in array for c in row)


if __name__ == '__main__':
    dots, instructions = load_instructions("day13_real_data.txt")
    array = make_dot_array(dots)
    axis, fold_position = instructions[0]
    array = fold(array, axis, fold_position)
    print("After 1 fold there are {} # marks on the paper.".format(count_dots(array)))

    for axis, fold_position in instructions[1:]:
        array = fold(array, axis, fold_position)
    print("After the remaining folds, the code is: ")
    print(draw_dots(array))
