from operator import add 
from tabletexifier.utils import compute_digits


class Table:
    def __init__(self, header, *args, **kwargs):
        self._header = header 
        self._lines = {col_name : [] for col_name in header}

        self._latex_properties = {'alignement': ['l' for _ in header],
                                  'lines': '||' }

        self._largest_entry = [len(head) for head in header]
        self.table_lines = {'T':[' ',''], '||':[' ',' |']}
        self.intersection_lines = {'T' : '-', '||' : '+'}

        
    def add_row(self, row):
        """
        Adds a new row to the table; Assumes that the order is the same as the one given in the header
        """
        for col_number, new_value in enumerate(row):
            if isinstance(new_value, str):
                entry_size = len(new_value)
            else:
                entry_size = compute_digits(new_value)
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
        except KeyError as e:
            raise Exception from e 

    def _get_table_info(self, col_number, fmt):
        """
            Return the charactcer that will separate two entries in a row. Return this separation on a column by column basis
        """
        line_type = self.table_lines[self._latex_properties['lines']]

        intersection = self.intersection_lines[self._latex_properties['lines']]
        
        if col_number == 0:
            if fmt == 'string':
                if self._latex_properties['lines'] == 'T':
                    line_type = [' ', ' |']
                    intersection = '+'
                elif self._latex_properties['lines'] == '||':
                    line_type = ['| ', ' |']
        if fmt == 'LaTeX':
            line_type = [' & ','']
            if col_number == 0:
                line_type = ['','']
            intersection = ''
        return line_type, intersection 


    def _add_horizontal_lines(self, all_rows, line_separator, fmt):
        output_lines = all_rows
        if fmt == 'string':
            if self._latex_properties['lines'] == 'T':
                output_lines.insert(1, line_separator)

            if self._latex_properties['lines'] == '||':
                table_edges = line_separator.replace("+",'-')
                out = [table_edges, output_lines[0]]
                for complete_line in output_lines[1:]:
                    out.append(line_separator)
                    out.append(complete_line)
                out.append(table_edges)
                output_lines = out 
        elif fmt == 'LaTeX':
            vlines = [] 
            output_lines = [line + r' \\' for line in output_lines]
            for index, _ in enumerate(self._header):
                if self._latex_properties['lines'] == 'T' and index == 0 or self._latex_properties['lines'] == '||':
                    vlines.append(r' \hline')
                else:
                    vlines.append(' ')
            output_lines = list(map( add, output_lines, vlines))

            if self._latex_properties['lines'] == '||':
                output_lines[0] = r'\hline' + output_lines[0]
        return output_lines

    def get_pretty_print(self, fmt = 'string'):

        line_entry = lambda value, line_type, spaces: '{1}{0}{3}{2}'.format(value, *line_type, ' '*spaces)
        
        line_type = self.table_lines[self._latex_properties['lines']]
        
        output_lines = [' ' for _ in range(self.N_lines+1)] # each line is an entry; Easy to add horizontal lines later one

        line_separator = ' ' +  self.intersection_lines[self._latex_properties['lines']]
        for col_number in range(self.N_columns):
            column = self.get_column(col_number, get_header=True)
            
            line_type, intersection = self._get_table_info(col_number, fmt)
            for line_index, col_entry in enumerate(column):
                entry = line_entry(col_entry, line_type,(self._largest_entry[col_number] -len(str(col_entry))))
                output_lines[line_index] = output_lines[line_index] + entry
            
            if col_number == 0:
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
        if self._latex_properties['lines'] == 'T':
            alg_str = ['','|'] + ['' for _ in self._header[2:]]
        if self._latex_properties['lines'] == '||':
            alg_str =  ['|' for _ in self._header]

        header = [r'\begin{table}',r'\caption{\label{Tab:}}',r'\begin{tabular}{' + ''.join(list(map(add,alg_str, self._latex_properties['alignement']))) + alg_str[-1]+'}']
        footer = [r'\end{tabular}', r'\end{table}']

        output_lines = self.get_pretty_print(fmt = 'LaTeX')
        return '\n'.join([*header,*output_lines, *footer])
            
    @property
    def N_columns(self):
        return len(self._header)
    
    @property
    def N_lines(self):
        return len(self._lines[self._header[0]])
     
    def latexify(self):
        pass 

    def __str__(self):
        return '\n'.join(self.get_pretty_print(fmt='string'))


