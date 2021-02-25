from tabletexifier.table_styles import Tlines, Alines, MNRAS, NoLines


class Table:
    def __init__(self, header, table_style='A'):

        self._style_map = {'T': Tlines, 'A': Alines, 'MNRAS': MNRAS, 'NoLines':NoLines}
        
        self._lines = [[col_name] for col_name in header]

        self._latex_properties = {'alignment': ['c' for _ in header],
                                  'style': table_style}

        self._table_style = self._style_map[self._latex_properties['style']]()
        self._journal_style = None

        self._largest_entry = [len(head) for head in header]

        # Number of decimal places in the numbers
        self._decimal_places = None

    def add_row(self, row):
        """
        Adds a new row to the table; Assumes that the order is the same as the one given in the header
        """
        for col_number, new_value in enumerate(row):

            entry_size = len(str(new_value))
            if entry_size > self._largest_entry[col_number]:
                self._largest_entry[col_number] = entry_size

            self._lines[col_number].append(new_value)

    def get_line(self, line_number):
        """
        Return an entire line; The line number is zero-indexed

        Parameters
        ===============
        line_number: int
            Line number to print; Zero-indexed; Does not count the header!!!
        """
        return [column[line_number] for column in self._lines]

    def delete_column(self, col_number):
        """
        Delete the column number associated with key
        """
        if self.N_columns <= 0:
            raise RuntimeError("Table has no columns")

        if col_number < 0 or col_number > self.N_columns -1 :
            raise IndexError("Column number {} does not exist".format(col_number)) 
        self._largest_entry.pop(col_number)
        self._lines.pop(col_number)

    def delete_row(self, row_number):
        """
        Delete a given row (the first non-header line is the first to be removed)
        """
        if self.N_lines <= 0:
            raise RuntimeError("Table has no lines of data")

        for index, column in enumerate(self._lines):
            _ = column.pop(row_number)
            # find the maximum size between the header and the largest element remaining in this column
            if len(column) > 0:
                self._largest_entry[index] = len(max([str(i) for i in column], key=len))
            else:
                self._largest_entry[index] = 0

    def get_column(self, key):
        """
            Return a column based on its index (starting at zero). 
        """
        if not isinstance(key, int) or key < 0 or key > self.N_columns :
            raise RuntimeError("Column -{}- does not exist".format(key))

        data_column = self._lines[key]
        return data_column

    def set_design_property(self, fmt_key, value):
        """
            Allow to configure the table properties. Currently available:
                fmt_key    |   value
                -----------+----------------------------------------------------
                style      |  A, T, MNRAS
                -----------+----------------------------------------------------
                alignment |  list with LaTeX possibilites for alignment or
                           |   a single value. If a list is provided, it must
                           |   have the alignment for each column. If a value
                           |  is passed then it will be applied to all columns

        """
        if fmt_key not in self._latex_properties:
            raise KeyError("Property {} does not exist".format(fmt_key))

        if fmt_key == 'alignment':
            valid_options = ['l', 'r', 'c']
            if isinstance(value, str):
                if value not in valid_options:
                    raise ValueError("LaTeX column alignment does not recognize {}".format(value))
                self._latex_properties['alignment'] = [value for _ in self._lines]
            elif isinstance(value, (tuple, list)):
                if any(elem not in valid_options for elem in value):
                    raise ValueError("LaTeX column alignment does not recognize {}".format(value))
                if len(value) != len(self._lines):
                    raise ValueError("Number of alignment properties different than the number of provided columns!")

                self._latex_properties['alignment'] = value

        if fmt_key == 'style':
            self._latex_properties[fmt_key] = value
            self._table_style = self._style_map[self._latex_properties['style']]()

    def _get_table_info(self, col_number, fmt):
        """
            Return the charactcer that will separate two entries in a row. Return this separation on a column by column basis
        """
        line_type = self._table_style.get_vline(col_number, fmt)
        intersection = self._table_style.get_intersection(col_number, fmt)[1]
        return line_type, intersection

    def _add_horizontal_lines(self, all_rows, line_separator, fmt):
        """
            Query the style class for the presence (or not) of a vertical separation between two consecutive lines in the table

            Parameters
            ----------
            all_rows: list
                List with the rows of data
            line_separator: str
                String build during the row creation. Used for the ASCII representation of the table
        """
        output_lines = all_rows

        out = []
        for index, row in enumerate(output_lines):
            vlines = self._table_style.get_hline(index, line_separator, fmt)
            out.append(vlines[0]+row+vlines[1])
        return out

    def get_pretty_print(self, ignore_cols, fmt='string'):

        line_entry = lambda value, line_type, spaces: '{1}{0}{3}{2}'.format(value, *line_type, ' '*spaces)

        output_lines = ['' for _ in range(self.N_lines)] # each line is an entry; Easy to add horizontal lines later one

        line_separator = '' + self._table_style.get_intersection(col_number=0, fmt=fmt)[0]
        ignore_cols = ignore_cols if ignore_cols is not None else []
        for col_number in range(self.N_columns):
            if col_number in ignore_cols:
                continue

            column = self.get_column(col_number)

            largest_entry = self._largest_entry[col_number]

            # update the column to find if there is a "rounded" integer with more places than the current largest element
            if self._decimal_places is not None:
                updated_column = []
                for col_entry in column:
                    if isinstance(col_entry, (int, float)):
                        col_entry = '{:.{}f}'.format(col_entry, self._decimal_places)
                    else:
                        col_entry = str(col_entry)
                    updated_column.append(col_entry)
                column = updated_column
                largest_entry = len(max(column, key = len))

            line_type, intersection = self._get_table_info(col_number, fmt)

            for line_index, col_entry in enumerate(column):
                entry = line_entry(col_entry, line_type, (largest_entry - len(str(col_entry))))
                output_lines[line_index] = output_lines[line_index] + entry

            if col_number == 0:  # account for the first edge separator, i.e. the first "|" or " "
                dashed_number = len(entry) - 2
            else:
                dashed_number = len(entry) - 1

            line_separator = line_separator + '-'*(dashed_number) + intersection

        output_lines = self._add_horizontal_lines(output_lines, line_separator, fmt)
        return output_lines

    def build_latex(self, ignore_cols=None):
        """
        Transform the table to LaTeX format and returns as a string, with each line seperated by a new line character
        """
        if ignore_cols is not None and not isinstance(ignore_cols, list):
            raise TypeError("ignore_cols must be a list.")

        center_prop = []
        if ignore_cols is  None:
            ignore_cols = []
        for col_index, _ in enumerate(self._lines):
            if ignore_cols is not None and col_index in ignore_cols:
                continue
            center_prop.append(self._latex_properties['alignment'][col_index])

        col_fmts = self._table_style.get_TeX_header(self.N_columns - len(ignore_cols), center_prop)

        header = [r'\begin{table}', r'\centering', r'\caption{\label{Tab:}}', r'\begin{tabular}{' + ''.join(col_fmts) + '}']
        footer = [r'\end{tabular}', r'\end{table}']

        output_lines = self.get_pretty_print(fmt='LaTeX', ignore_cols=ignore_cols)
        return '\n'.join([*header, *output_lines, *footer])

    def set_decimal_places(self, value):
        if not isinstance(value, int):
            raise TypeError("The decimal places must be an integer")
        self._decimal_places = value

    def write_to_file(self, path, mode='a', write_table=True, write_LaTeX=False, ignore_cols=None):

        with open(path, mode=mode) as file:
            if write_table:
                lines = self.get_pretty_print(fmt='string', ignore_cols=ignore_cols)
                file.write(''.join(lines))
            if write_LaTeX:
                if write_table:
                    file.write('\n')
                lines = self.build_latex()
                file.write(lines)

    @property
    def N_columns(self):
        return len(self._lines)

    @property
    def N_lines(self):
        if self.N_columns <= 0:
            return 0
        return len(self._lines[0])

    def __str__(self):
        return ''.join(self.get_pretty_print(fmt='string', ignore_cols=[]))
