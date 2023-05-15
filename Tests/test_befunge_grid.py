import pytest
from befunge import befunge_grid


def test_grid_from_string_list():
    grid = befunge_grid.BefungeGrid()
    string_list = [">>v", "^<<"]
    grid.set_grid("s", string_list)
    assert grid.grid == string_list


def test_debug_mode(capfd):
    grid = befunge_grid.BefungeGrid()
    string_list = ["@"]
    grid.set_grid("s", string_list)
    grid.run(True)
    out, err = capfd.readouterr()
    debug_out = "evaluate command [ @ ]"\
                " at Y: 1 X: 1, string mode: False, stack: [  ]\n"
    assert out == debug_out
    assert err == ""


def test_string_mode():
    grid = befunge_grid.BefungeGrid()
    string_list = ['"qwerty"@']
    grid.set_grid("s", string_list)
    grid.run()
    assert "".join(chr(e) for e in grid.stack) == string_list[0][1:-2]


def test_numbers_into_stack():
    grid = befunge_grid.BefungeGrid()
    string_list = ["123@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert [1, 2, 3] == grid.stack


@pytest.mark.parametrize("test_input,expected",
                         [(["23-@"], 1),
                          (["-@"], 0),
                          (["*@"], 0),
                          (["26/@"], 3),
                          (["/@"], 0),
                          (["03/@"], 0),
                          (["49%@"], 1),
                          (["%@"], 0),
                          (["00%@"], 0),
                          (["1!@"], 0),
                          (["0!@"], 1),
                          (["!@"], 0),
                          (["12`@"], 0),
                          (["21`@"], 1),
                          (["`@"], 0)])
def test_arithmetic_commands_result_on_top_of_the_stack(test_input, expected):
    grid = befunge_grid.BefungeGrid()
    string_list = test_input
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack[-1] == expected


@pytest.mark.parametrize("test_input,expected",
                         [(["+@"], [0]),
                          (["1:@"], [1, 1]),
                          ([":@"], [0, 0]),
                          (["12\\@"], [2, 1]),
                          (["\\@"], [0, 0]),
                          (["1$@"], []),
                          (["$@"], [])])
def test_arithmetic_commands_result_full_stack(test_input, expected):
    grid = befunge_grid.BefungeGrid()
    string_list = test_input
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack == expected


def test_sharp_command():
    grid = befunge_grid.BefungeGrid()
    grid.set_grid("s", ["#@v", "  @"])
    grid.run()
    assert grid.y == 1
    assert grid.x == 2


def test_output_dot_command(capfd):
    """output dot (.) test"""
    grid = befunge_grid.BefungeGrid()
    string_list = ["1.@"]
    grid.set_grid("s", string_list)
    grid.run()
    out, err = capfd.readouterr()
    assert out == "1 "


def test_output_comma_command(capfd):
    """output comma (,) test"""
    grid = befunge_grid.BefungeGrid()
    string_list = ["9,@"]  # 9 is a code for tab symbol
    grid.set_grid("s", string_list)
    grid.run()
    out, err = capfd.readouterr()
    assert out == "\t"


def test_input_ampersand_command(monkeypatch):
    """input ampersand (&) test"""
    monkeypatch.setattr('builtins.input', lambda: 1)
    grid = befunge_grid.BefungeGrid()
    string_list = ["&@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack[0] == 1


def test_input_tilda_command(monkeypatch):
    """input tilda (~) test"""
    monkeypatch.setattr('builtins.input', lambda: "\t")
    grid = befunge_grid.BefungeGrid()
    string_list = ["~@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack[0] == 9


def test_invalid_operand(capfd):
    """output after invalid operand test"""
    grid = befunge_grid.BefungeGrid()
    string_list = ["Z"]
    grid.set_grid("s", string_list)
    grid.run()
    out, err = capfd.readouterr()
    assert out == "Invalid operand [ Z ] at 1 row, 1 column\n"


def test_put_command():
    grid = befunge_grid.BefungeGrid()
    string_list = ["67+5*11p@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.grid[0][0] == "A"


def test_put_command_empty_stack():
    grid = befunge_grid.BefungeGrid()
    string_list = ["p@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.grid[0][0] == "0"


def test_get_command():
    grid = befunge_grid.BefungeGrid()
    string_list = ["21g@", "  A "]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack[-1] == 65


def test_get_command_empty_stack():
    grid = befunge_grid.BefungeGrid()
    string_list = ["g@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack[-1] == 0


@pytest.mark.parametrize("test_input,expected",
                         [([">@"], [1, 0]),
                          (["^ ", "@ "], [0, 1]),
                          (["<@"], [1, 0]),
                          (["v ", "@ "], [0, 1]),
                          (["1|", " @", " @"], [1, 2]),
                          (["0|", " @", " @"], [1, 1]),
                          (["1v ", "@_@"], [0, 1]),
                          (["0v ", "@_@"], [2, 1])])
def test_moving(test_input, expected):
    grid = befunge_grid.BefungeGrid()
    string_list = test_input
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.x == expected[0]
    assert grid.y == expected[1]


def test_random_moving():
    grid = befunge_grid.BefungeGrid()
    string_list = ["?@", "@ "]
    grid.set_grid("s", string_list)
    grid.run()
    assert (grid.x == 0 and grid.y == 1) or (grid.x == 1 and grid.y == 0)
