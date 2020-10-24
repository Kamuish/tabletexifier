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

    expected_col = ['first', 'second', 'third']
    for key in ['Name', 0]:
        pytest.assume(all([a == b for a, b in zip(x.get_column(key, get_header=False), expected_col)]))
    expected_col = ['Name', 'first', 'second', 'third']
    for key in ['Name', 0]:
        pytest.assume(all([a == b for a, b in zip(x.get_column(key, get_header=True), expected_col)]))


def test_remove_data():

    x = Table(['Name', 'b','c','d','e']) 
    row_1 = ['first',1,4,6,7]
    x.add_row(row_1)

    pytest.assume(x.N_lines == 1)
    x.delete_row(0)
    x.delete_column("b")
    pytest.assume(x.N_lines == 0)
    pytest.assume(x.N_columns == 4)

    for k in ['Name', 'c', 'd','e']:
        x.delete_column(k)

    pytest.assume(x.N_columns == 0)

    with pytest.raises(RuntimeError) as execinfo:
        x.delete_row(0)
     
    assert execinfo.value.args[0] == 'Table has no lines of data'