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
    
    key = 'Name'
    pytest.assume(all([a == b for a, b in zip(x[key], expected_col)]))
    with pytest.raises(TypeError) as execinfo:
        _ = x[0]
    assert execinfo.value.args[0] == 'Key should be a string'

    
    expected_col = ['Name', 'first', 'second', 'third']
    for key in ['Name', 0]:
        pytest.assume(all([a == b for a, b in zip(x.get_column(key, get_header=True), expected_col)]))


    for col_numb in [-1, 100, 'fourth']:
        with pytest.raises(RuntimeError) as execinfo:
            x.get_column(col_numb)
        assert execinfo.value.args[0] == 'Column -{}- does not exist'.format(col_numb)
    
    with pytest.raises(ValueError) as execinfo:
        x.get_column(['FOURTH'])
    assert execinfo.value.args[0] == 'Invalid identifier for the column;'
   

def test_remove_column():

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
    
    with pytest.raises(RuntimeError) as execinfo:
        x.delete_column(0)
    assert execinfo.value.args[0] == 'Table has no columns'

def test_remove_row():
    x = Table(['Name', 'b','c','d','e']) 
    x.add_row( ['first',1,4,6,7])
    x.add_row( ['second',1,4,6,7])

    assert x._largest_entry[0] == 6
    x.delete_row(1)
    assert x._largest_entry[0] == 5

def test_decimals():

    x = Table(['Name', 'b','c','d','e']) 
    row_1 = ['first',1,4,6,7]
    x.add_row(row_1)

    for val in ['1', [1], None]:
        print('entry: ', val, type(val))
        with pytest.raises(TypeError) as execinfo:
            x.set_decimal_places(val)
        assert execinfo.value.args[0] == 'The decimal places must be an integer'

    x.set_decimal_places(5)
    assert x._decimal_places == 5