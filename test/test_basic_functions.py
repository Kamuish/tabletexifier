from tabletexifier import Table 
import pytest

def test_load_data():

    x = Table(['Name', 'b','c','d','e']) 
    x.add_row(['first',1,4,6,7])
    x.add_row(['second',1,4,6,7])

    pytest.assume(x.N_columns == 5)
    pytest.assume(x.N_lines == 2)

    x.add_row(['third',5,6,7,8])
    pytest.assume(x.N_lines == 3)

def test_retrieve_data():

    x = Table(['Name', 'b','c','d','e']) 
    row_1 = ['first',1,4,6,7]
    x.add_row(row_1)
    x.add_row(['second',1,4,6,7])
    x.add_row(['third',5,6,7,8])

    pytest.assume(all([a == b for a, b in zip(x.get_line(0), row_1)]))
