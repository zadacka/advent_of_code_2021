import copy
import os


def load_day20_data(filename):
    algorithm = ""
    image = []
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        algorithm = f.readline().strip()
        _ = f.readline()

        for line in f.readlines():
            image.append([c for c in line.strip()])

    return algorithm, image


def pad_image(input_image, pad=3):
    columns = len(input_image[0])
    full_column = ["." for _ in range(columns + 2 * pad)]
    side_padding = ["." for _ in range(pad)]

    result = []
    for i in range(pad):
        result.append(copy.deepcopy(full_column))
    for column in input_image:
        result.append(copy.deepcopy(side_padding) + copy.deepcopy(column) + copy.deepcopy(side_padding))
    for i in range(pad):
        result.append(copy.deepcopy(full_column))
    return result


def trim_image(input_image, trim=1):
    return [[pixel for pixel in row[trim:-trim]] for row in input_image[trim:-trim]]


def output_image(image):
    result = ""
    for row in image:
        result += ''.join(row) + '\n'
    return result


def get_neighbour_values(r, c, input_image):
    max_row = len(input_image)
    max_col = len(input_image[0])
    neighbours = [
        (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
        (r, c - 1), (r, c), (r, c + 1),
        (r + 1, c - 1), (r + 1, c), (r + 1, c + 1),
    ]
    return [input_image[r][c] if 0 <= r < max_row and 0 <= c < max_col else "." for r, c in neighbours]


def enhance_image(input_image, algorithm):
    """ To cope with imaging artefacts at the edge, we only enhance from 1:-1 within the input, and then pad """
    result = []
    for row_index, row in enumerate(input_image):
        new_row = []
        for column_index, element in enumerate(row):
            neighbour_values = get_neighbour_values(row_index, column_index, input_image)
            index = get_index(neighbour_values)
            new_value = algorithm[index]
            new_row.append(new_value)
        result.append(new_row)
    return result


def get_index(pixels):
    binary = ''.join(['0' if pixel == '.' else '1' for pixel in pixels])
    return int(binary, base=2)


def count_pixels(image):
    return sum(pixel == "#" for row in image for pixel in row)


if __name__ == '__main__':
    algorithm, image = load_day20_data("day20_real_data.txt")
    padded_image = pad_image(image, 10)
    enhanced = enhance_image(input_image=padded_image, algorithm=algorithm)
    enhanced_again = enhance_image(input_image=enhanced, algorithm=algorithm)
    print(f"There are {count_pixels(enhanced_again)} pixels on in the twice enhanced image.")

    # the pixels in the original image can grow outwards by 1 pixel/cycle
    # ... 50 cycles = 50 extra pixels needed for padding

    # edge effects mean that we need to trim the edge of the enhanced image by 1 pixel/cycle
    # ... 50 cycles = need to trim 50 pixels per edge in total

    # so ... add 100 pixels in padding to start with

    very_padded_image = pad_image(image, 100)
    for _ in range(50):
        very_padded_image = enhance_image(very_padded_image, algorithm)
        very_padded_image = trim_image(very_padded_image, 1)
    print(f"There are {count_pixels(very_padded_image)} pixels on in the fifty times enhanced image.")
