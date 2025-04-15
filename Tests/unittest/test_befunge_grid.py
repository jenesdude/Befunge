import unittest
from io import StringIO
from unittest.mock import patch
from befunge import befunge_grid


class TestBefungeGrid(unittest.TestCase):
    def test_grid_from_string_list(self):
        grid = befunge_grid.BefungeGrid()
        string_list = [">>v", "^<<"]
        grid.set_grid("s", string_list)
        self.assertEqual(grid.grid, string_list)

    def test_debug_mode(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["@"]
        grid.set_grid("s", string_list)
        with patch("sys.stdout", new_callable=StringIO) as out:
            with patch("sys.stderr", new_callable=StringIO) as err:
                grid.run(True)
                debug_out = "evaluate command [ @ ]" \
                            " at Y: 1 X: 1, string mode: False, stack: [  ]\n"
                self.assertIn(debug_out, out.getvalue())
                self.assertEqual("", err.getvalue())

    def test_string_mode(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ['"qwerty"@']
        grid.set_grid("s", string_list)
        grid.run()
        self.assertEqual("".join(chr(e) for e in grid.stack), string_list[0][1:-2])

    def test_numbers_into_stack(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["123@"]
        grid.set_grid("s", string_list)
        grid.run()
        self.assertEqual([1, 2, 3], grid.stack)

    def test_arithmetic_commands_result_on_top_of_the_stack(self):
        test_cases = [
            (["23-@"], 1),
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
            (["`@"], 0)
        ]

        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input, expected=expected):
                grid = befunge_grid.BefungeGrid()
                grid.set_grid("s", test_input)
                grid.run()
                self.assertEqual(grid.stack[-1], expected)

    def test_arithmetic_commands_result_full_stack(self):
        test_cases = [
            (["+@"], [0]),
            (["1:@"], [1, 1]),
            ([":@"], [0, 0]),
            (["12\\@"], [2, 1]),
            (["\\@"], [0, 0]),
            (["1$@"], []),
            (["$@"], [])
        ]

        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input, expected=expected):
                grid = befunge_grid.BefungeGrid()
                string_list = test_input
                grid.set_grid("s", string_list)
                grid.run()
                self.assertEqual(grid.stack, expected)

    def test_sharp_command(self):
        grid = befunge_grid.BefungeGrid()
        grid.set_grid("s", ["#@v", "  @"])
        grid.run()
        self.assertEqual(grid.y, 1)
        self.assertEqual(grid.x, 2)

    def test_output_commands(self):
        test_cases = [
            (["1.@"], "1 "),  # output dot '.' test
            (["9,@"], "\t")  # output comma ',' test
        ]

        for test_input, expected in test_cases:
            with self.subTest(test_input=test_input, expected=expected):
                with patch("sys.stdout", new_callable=StringIO) as out:
                    with patch("sys.stderr", new_callable=StringIO) as err:
                        grid = befunge_grid.BefungeGrid()
                        string_list = test_input
                        grid.set_grid("s", string_list)
                        grid.run()
                        self.assertIn(expected, out.getvalue())
                        self.assertEqual("", err.getvalue())

    @patch('sys.stdin', StringIO("1"))
    def test_input_ampersand_command(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["&@"]
        grid.set_grid("s", string_list)
        grid.run()
        self.assertEqual(grid.stack[0],1)

    @patch('sys.stdin', StringIO("\t"))
    def test_input_tilda_command(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["~@"]
        grid.set_grid("s", string_list)
        grid.run()
        self.assertEqual(grid.stack[0], 9)

    def test_invalid_operand(self):
        with patch("sys.stdout", new_callable=StringIO) as out:
            with patch("sys.stderr", new_callable=StringIO) as err:
                grid = befunge_grid.BefungeGrid()
                string_list = ["Z"]
                grid.set_grid("s", string_list)
                grid.run()
                expected_out = "Invalid operand [ Z ] at 1 row, 1 column\n"
                self.assertEqual(expected_out, out.getvalue())
                self.assertEqual("", err.getvalue())

    def test_put_command(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["67+5*11p@"]
        grid.set_grid("s", string_list)
        grid.run()
        assert grid.grid[0][0] == "A"

    def test_put_command_empty_stack(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["p@"]
        grid.set_grid("s", string_list)
        grid.run()
        assert grid.grid[0][0] == "0"

    def test_get_command(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["21g@", "  A "]
        grid.set_grid("s", string_list)
        grid.run()
        assert grid.stack[-1] == 65

    def test_get_command_empty_stack(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["g@"]
        grid.set_grid("s", string_list)
        grid.run()
        assert grid.stack[-1] == 0

    def test_moving(self):
        test_cases = [
            ([">@"], [1, 0]),
            (["^ ", "@ "], [0, 1]),
            (["<@"], [1, 0]),
            (["v ", "@ "], [0, 1]),
            (["1|", " @", " @"], [1, 2]),
            (["0|", " @", " @"], [1, 1]),
            (["1v ", "@_@"], [0, 1]),
            (["0v ", "@_@"], [2, 1])
        ]

        for test_input, expected in test_cases:
            grid = befunge_grid.BefungeGrid()
            string_list = test_input
            grid.set_grid("s", string_list)
            grid.run()
            self.assertEqual(grid.x, expected[0])
            self.assertEqual(grid.y, expected[1])

    def test_random_moving(self):
        grid = befunge_grid.BefungeGrid()
        string_list = ["?@", "@ "]
        grid.set_grid("s", string_list)
        grid.run()
        assert (grid.x == 0 and grid.y == 1) or (grid.x == 1 and grid.y == 0)
