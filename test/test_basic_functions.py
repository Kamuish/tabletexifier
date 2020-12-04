import pytest
from tabletexifier import Table


def test_load_data():

    x = Table(['Name', 'b', 'c', 'd', 'e'])
    x.add_row(['first', 1, 4, 6, 7])
    x.add_row(['second', 1, 4, 6, 7])

    pytest.assume(x.N_columns == 5)
    pytest.assume(x.N_lines == 3)

    x.add_row(['third', 5, 6, 7, 8])
    pytest.assume(x.N_lines == 4)


def test_retrieve_data():

    x = Table(['Name', 'b', 'c', 'd', 'e'])
    row_1 = ['first', 1, 4, 6, 7]
    x.add_row(row_1)
    x.add_row(['second', 1, 4, 6, 7])
    x.add_row(['third', 5, 6, 7, 8])

    pytest.assume(all([a == b for a, b in zip(x.get_line(1), row_1)]))

    expected_col = ['Name', 'first', 'second', 'third']
    for key in [0]:
        pytest.assume(all([a == b for a, b in zip(x.get_column(key), expected_col)]))

    for col_numb in [-1, 100, 'fourth']:
        with pytest.raises(RuntimeError) as execinfo:
            x.get_column(col_numb)
        assert execinfo.value.args[0] == 'Column -{}- does not exist'.format(col_numb)


def test_delete_column():

    x = Table(['Name', 'b', 'c', 'd', 'e'])

    pytest.assume(x.N_lines == 1)
    x.delete_row(0)
    x.delete_column(1)
    pytest.assume(x.N_lines == 0)
    pytest.assume(x.N_columns == 4)

    for _ in range(4):
        x.delete_column(0)

    pytest.assume(x.N_columns == 0)

    with pytest.raises(RuntimeError) as execinfo:
        x.delete_row(0)
    assert execinfo.value.args[0] == 'Table has no lines of data'

    with pytest.raises(RuntimeError) as execinfo:
        x.delete_column(0)
    assert execinfo.value.args[0] == 'Table has no columns'


def test_delete_row():
    x = Table(['Name', 'b', 'c', 'd', 'e'])
    x.add_row(['first', 1, 4, 6, 7])
    x.add_row(['second', 1, 4, 6, 7])

    assert x._largest_entry[0] == 6
    x.delete_row(2)
    assert x._largest_entry[0] == 5


def test_set_design_property():
    x = Table(['Name', 'b', 'c', 'd', 'e'])

    prop_name = 1
    with pytest.raises(KeyError) as execinfo:
        x.set_design_property(prop_name, 0)
    assert execinfo.value.args[0] == "Property {} does not exist".format(prop_name)


def test_build_latex():
    x = Table(['Name', 'b', 'c', 'd', 'e'])
    x.add_row(['first', 1, 4, 6, 7])

    result_all_cols = r"""\begin{table}
\centering
\caption{\label{Tab:}}
\begin{tabular}{|c|c|c|c|c|}
\hline
  Name  & b & c & d & e \\ \hline
  first & 1 & 4 & 6 & 7 \\ \hline
\end{tabular}
\end{table}"""

    assert x.build_latex() == result_all_cols

    result_no_name = r"""\begin{table}
\centering
\caption{\label{Tab:}}
\begin{tabular}{|c|c|c|c|}
\hline
  & b & c & d & e \\ \hline
  & 1 & 4 & 6 & 7 \\ \hline
\end{tabular}
\end{table}"""

    assert x.build_latex(ignore_cols=[0]) == result_no_name

    with pytest.raises(TypeError) as execinfo:
        x.build_latex(ignore_cols='Name')
    assert execinfo.value.args[0] == "ignore_cols must be a list."


def test_set_decimal_places():

    x = Table(['Name', 'b', 'c', 'd', 'e'])
    row_1 = ['first', 1, 4, 6, 7]
    x.add_row(row_1)

    for val in ['1', [1], None]:
        print('entry: ', val, type(val))
        with pytest.raises(TypeError) as execinfo:
            x.set_decimal_places(val)
        assert execinfo.value.args[0] == 'The decimal places must be an integer'

    x.set_decimal_places(5)
    assert x._decimal_places == 5


def test_write_to_file(tmpdir):
    x = Table(['Name', 'b', 'c', 'd', 'e'])
    row_1 = ['first', 1, 4, 6, 7]
    x.add_row(row_1)

    file = tmpdir.join('output.txt')
    x.write_to_file(file.strpath)
    assert file.read() == ''.join(x.get_pretty_print(None))

    file = tmpdir.join('output_both.txt')
    x.write_to_file(file.strpath, write_LaTeX=True)
    assert file.read() == ''.join(x.get_pretty_print(None)) + '\n' + x.build_latex()

    file = tmpdir.join('output_latex.txt')
    x.write_to_file(file.strpath, write_table=False, write_LaTeX=True)
    assert file.read() == x.build_latex()
