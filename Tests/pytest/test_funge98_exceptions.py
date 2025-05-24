import pytest
from funge98 import funge98, funge98_exceptions


def test_instruction_pointer_is_in_wrong_dimension_error():
    with pytest.raises(funge98_exceptions.IPHasInWrongDimensionError):
        space = funge98.FungeSpace(2)
        space.stack.begin_block(space, [0])
