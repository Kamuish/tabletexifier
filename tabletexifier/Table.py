from operator import add 
from tabletexifier.table_styles import Tlines, Alines, MNRAS

class Table:
    def __init__(self, header, table_style = 'A' ,*args, **kwargs):

        self._style_map = {'T': Tlines, 'A':Alines, 'MNRAS':MNRAS}
        self._header = header 
        self._lines = {col_name : [] for col_name in header}

        self._latex_properties = {'alignement': ['c' for _ in header],
                                  'lines': table_style }

        self._table_style = self._style_map[self._latex_properties['lines']]()
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

            self._lines[self._header[col_number]].append(new_value)

    def get_line(self, line_number):
        """
        Return an entire line; The line number is zero-indexed

        Parameters
        ===============
        line_number: int 
            Line number to print; Zero-indexed; Does not count the header!!!
        """
        return [column[line_number] for column in self._lines.values()]

    def get_column(self, col_number, get_header = False):

        out = self._header[col_number] if get_header else ''
        return [out] + self._lines[self._header[col_number]]

    def set_design_property(self, fmt_key, value):
        try:
            self._latex_properties[fmt_key] = value 

            if fmt_key == 'lines':
                self._table_style = self._style_map[self._latex_properties['lines']]()
  
        except KeyError as e:
            raise Exception from e 

    def _get_table_info(self, col_number, fmt):
        """
            Return the charactcer that will separate two entries in a row. Return this separation on a column by column basis
        """
        line_type = self._table_style.get_vline(col_number, fmt)
        intersection = self._table_style.get_intersection(col_number, fmt)[1]
        return line_type, intersection 



    def _add_horizontal_lines(self, all_rows, line_separator, fmt):
        output_lines = all_rows

        out = []
        for index, row in enumerate(output_lines):
            vlines = self._table_style.get_hline(index, line_separator, fmt)
            out.append(vlines[0]+row+vlines[1])
        return out 


    def get_pretty_print(self, fmt = 'string'):

        line_entry = lambda value, line_type, spaces: '{1}{0}{3}{2}'.format(value, *line_type, ' '*spaces)
        
        
        output_lines = [' ' for _ in range(self.N_lines+1)] # each line is an entry; Easy to add horizontal lines later one

        line_separator = ' ' +  self._table_style.get_intersection(col_number=0, fmt = fmt)[0]

        for col_number in range(self.N_columns):
            column = self.get_column(col_number, get_header=True)

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
                entry = line_entry(col_entry, line_type,(largest_entry -len(str(col_entry))))
                output_lines[line_index] = output_lines[line_index] + entry
            
            if col_number == 0: # account for the first edge separator, i.e. the first "|" or " "
                dashed_number = len(entry) - 2 
            else:
                dashed_number = len(entry) - 1
                
            line_separator = line_separator + '-'*(dashed_number) +intersection

        output_lines = self._add_horizontal_lines(output_lines, line_separator, fmt)
        return output_lines

    def build_latex(self):
        """
        Transform the table to LaTeX format and returns as a string, with each line seperated by a new line character
        """

        col_fmts = self._table_style.get_TeX_header(self._header, self._latex_properties['alignement'])

        header = [r'\begin{table}',r'\centering',r'\caption{\label{Tab:}}',r'\begin{tabular}{' + ''.join(col_fmts) +'}']
        footer = [r'\end{tabular}', r'\end{table}']

        output_lines = self.get_pretty_print(fmt = 'LaTeX')
        return '\n'.join([*header,*output_lines, *footer])

    def set_decimal_places(self, value):
        self._decimal_places = value 

    def write_to_file(self, path, mode='a', write_table = True, write_LaTeX=False):

        with open(path, mode = mode) as file:
            if write_table:
                lines = self.get_pretty_print(fmt = 'string')
                file.write(''.join(lines) + '\n')
            if write_LaTeX:
                lines = self.build_latex()
                file.write(lines)  

    @property
    def N_columns(self):
        return len(self._header)
    
    @property
    def N_lines(self):
        return len(self._lines[self._header[0]])
     
    def __str__(self):
        return ''.join(self.get_pretty_print(fmt='string'))


