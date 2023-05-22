import pytest
from funge98 import funge98, funge98_exceptions


def test_instruction_pointer_is_in_wrong_dimension_error():
    with pytest.raises(funge98_exceptions.IPHasInWrongDimensionError):
        grid = funge98.FungeSpace()
        grid.stack.begin_block([0])
