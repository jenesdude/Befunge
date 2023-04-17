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
    assert out == "evaluate command [ @ ] at Y: 1 X: 1, string mode: False, stack: [  ]\n"
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


def test_arithmetic_commands_empty_stack():
    grid = befunge_grid.BefungeGrid()
    grid.set_grid("s", ["+@"])
    grid.run()
    assert grid.stack[0] == 0

    grid.set_grid("s", ["23-@"])
    grid.run()
    assert grid.stack[-1] == 1

    grid.set_grid("s", ["-@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["*@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["26/@"])
    grid.run()
    assert grid.stack[-1] == 3

    grid.set_grid("s", ["/@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["03/@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["49%@"])
    grid.run()
    assert grid.stack[-1] == 1

    grid.set_grid("s", ["%@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["00%@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["1!@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["0!@"])
    grid.run()
    assert grid.stack[-1] == 1

    grid.set_grid("s", ["!@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["1:@"])
    grid.run()
    assert grid.stack == [1, 1]

    grid.set_grid("s", [":@"])
    grid.run()
    assert grid.stack == [0, 0]

    grid.set_grid("s", ["12`@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["21`@"])
    grid.run()
    assert grid.stack[-1] == 1

    grid.set_grid("s", ["`@"])
    grid.run()
    assert grid.stack[-1] == 0

    grid.set_grid("s", ["12\\@"])
    grid.run()
    assert grid.stack == [2, 1]

    grid.set_grid("s", ["\\@"])
    grid.run()
    assert grid.stack == [0, 0]

    grid.set_grid("s", ["1$@"])
    grid.run()
    assert grid.stack == []

    grid.set_grid("s", ["$@"])
    grid.run()
    assert grid.stack == []

    # grid.set_grid("s", ["?@", "@ "])
    # grid.run()
    # assert (grid.y == 0 and grid.x == 1) or (grid.y == 1 and grid.x == 0)

    # grid.set_grid("s", ["1|", " @"])
    # grid.run()
    # assert grid.y == 1
    # assert grid.x == 1

    # grid.set_grid("s", ["0|", " @", "  "])
    # grid.run()
    # assert grid.y == 1
    # assert grid.x == 1


def test_sharp_command():
    grid = befunge_grid.BefungeGrid()
    grid.set_grid("s", ["#@v", "  @"])  # end in # at the second string
    grid.run()
    assert grid.y == 1
    assert grid.x == 2


def test_output_dot_command(capfd):
    grid = befunge_grid.BefungeGrid()
    string_list = ["1.@"]
    grid.set_grid("s", string_list)
    grid.run()
    out, err = capfd.readouterr()
    assert out == "1 "


def test_output_comma_command(capfd):
    grid = befunge_grid.BefungeGrid()
    string_list = ["9,@"]  # 9 is a code for tab symbol
    grid.set_grid("s", string_list)
    grid.run()
    out, err = capfd.readouterr()
    assert out == "\t"


def test_input_ampersand_command(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: 1)
    grid = befunge_grid.BefungeGrid()
    string_list = ["&@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack[0] == 1


def test_input_tilda_command(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: "\t")
    grid = befunge_grid.BefungeGrid()
    string_list = ["~@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.stack[0] == 9


def test_invalid_operand(capfd):
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


def test_move_right():
    grid = befunge_grid.BefungeGrid()
    string_list = [">@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.x == 1
    assert grid.y == 0


def test_move_up():
    grid = befunge_grid.BefungeGrid()
    string_list = ["^ ", "@ "]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.x == 0
    assert grid.y == 1


def test_move_left():
    grid = befunge_grid.BefungeGrid()
    string_list = ["<@"]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.x == 1
    assert grid.y == 0


def test_move_down():
    grid = befunge_grid.BefungeGrid()
    string_list = ["v ", "@ "]
    grid.set_grid("s", string_list)
    grid.run()
    assert grid.x == 0
    assert grid.y == 1
