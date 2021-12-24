
from testfixtures import compare

from day24.day24 import load_day_24_data, Alu

test_input_steps = [
    ("inp", "w", None),
    ("add", "z", "w"),
    ("mod", "z", 2),
    ("div", "w", 2),
    ("add", "y", "w"),
    ("mod", "y", 2),
    ("div", "w", 2),
    ("add", "x", "w"),
    ("mod", "x", 2),
    ("div", "w", 2),
    ("mod", "w", 2),
]
def test_load_day24_data():
    compare(load_day_24_data("day24_test_data.txt"), expected=test_input_steps)

def test_alu_methods():
    alu = Alu("12345", [])
    alu.input("x")
    compare(alu.x, expected=1)
    alu.input("y")
    compare(alu.y, expected=2)
    alu.add('z', 10)
    compare(alu.z, expected=10)
    alu.add('z', 'x')
    compare(alu.z, expected=11)

    alu.mul('z', 2)
    compare(alu.z, expected=22)

    alu.div('z', 3)
    compare(alu.z, expected=7)
    alu.div('z', 2)
    compare(alu.z, expected=3)  # integer, rounding down

    alu.add('z', 2)
    alu.mod('z', 3)
    compare(alu.z, expected=2)

    alu.eql('z', 2)
    compare(alu.z, expected=1)
    alu.eql('z', 7)
    compare(alu.z, expected=0)

def test_perform_alu_steps():
    alu = Alu('9', steps=test_input_steps)
    alu.do_steps()
    compare(alu.w, expected=1)
    compare(alu.x, expected=0)
    compare(alu.y, expected=0)
    compare(alu.z, expected=1)

def test_doing_it():
    steps = load_day_24_data("day24_real_data.txt")
    for potential_model_number in range(99999999999999, 0, -1):
        str_model_no = str(potential_model_number)
        if '0' in str_model_no:
            continue
        else:
            print(str_model_no)
            alu = Alu(str_model_no, steps)
            alu.do_steps()
            if alu.z == 0:
                print(f"The submarine model is {str_model_no}")
                break