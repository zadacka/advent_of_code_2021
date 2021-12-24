import os.path
from collections import deque


def load_day_24_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath) as f:
        text = f.readlines()
    op2operator = {
        "add": '+=',
        "mul": '*=',
        "div": '//=',
        "mod": '%=',
    }
    result = ["global w, x, y, z", "w, x, y, z,  = 0, 0, 0, 0"]
    for line in text:
        if line.startswith("inp"):
            result.append("w = candidate.popleft()\n")
        elif line[0:3] in op2operator:
            result.append(f"{line[4]} {op2operator[line[0:3]]} {line[6:]}")
        else:
            result.append(f"{line[4]} = 1 if {line[4]} == {line[6:-1].strip()} else 0")
    return '\n'.join([r.strip() for r in result])

def compute(candidate):
    str_candidate = str(candidate)
    if '0' in str_candidate:
        return None, None, None, None
    # print(str_candidate)
    candidate = deque([int(c) for c in str_candidate])
    exec(steps)
    # print(f"now w={w}, x={x}, y={y}, z={z}")
    return w, x, y, z



if __name__ == '__main__':
    steps = load_day_24_data("day24_real_data.txt")
    for potential_model_number in range(99999999999999, 0, -1):
        w, x, y, z = compute(potential_model_number)
        if z == 0:
            print(f"****** {potential_model_number} ********")
            break
    #     str_model_no = str(potential_model_number)
    #     if '0' in str_model_no:
    #         continue
    #     else:
    #         # print(f'trying {str_model_no}')
    #         alu = Alu(str_model_no, steps)
    #         alu.do_steps()
    #         if alu.z == 0:
    #             print(f"The submarine model is {str_model_no}")
    #             break
