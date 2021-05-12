from operator import add


class Style:
    def __init__(self):
        pass

    def get_vline(self, col_number, fmt):
        """
        Return vline separator for a given column. Returns an array with the separator for the left and right
        """
        pass

    def get_hline(self, row_number, separator, fmt):
        """
        Return horizontal separator for a given column. Returns an array with the separator for the above and below
        """
        pass

    def get_intersection(self, col_number, fmt):
        pass

    def _build_header_vlines(self, v_fmt, alignment):
        return list(map(add, v_fmt, alignment)) + [v_fmt[-1]]


class Tlines(Style):
    def get_vline(self, col_number, fmt):
        out = [' ', '']
        if fmt == 'string':
            if col_number == 0:
                out = [' ', ' |']
        elif fmt == 'LaTeX':
            if col_number == 0:
                out = [' ', '']
            else:
                out = [' & ', '']

        return out

    def get_hline(self, row_number, separator, fmt):
        out = ['', '\n']
        if row_number == 0:
            if fmt == 'string':
                out = ['', '\n' + separator + '\n']
        if fmt == 'LaTeX':
            if row_number == 0:
                out = ['', r' \\ \hline']
            else:
                out = ['', r' \\']
        return out

    def get_intersection(self, col_number, fmt):

        if fmt == 'string':
            separation = ['-', '+'] if col_number == 0 else ['-', '-']
        elif fmt == 'LaTeX':
            separation = ['&', '&']
        return separation

    def get_TeX_header(self, head_size, alignment):
        alg_str = ['|' for _ in range(head_size)]

        return self._build_header_vlines(alg_str, alignment)


class Alines(Style):
    def get_vline(self, col_number, fmt):
        """
        Return vline separator for a given column. Returns an array with the separator for the left and right
        """
        out = ['', '']
        if fmt == 'string':
            out = [' ', ' |']
            if col_number == 0:
                out = ['| ', ' |']
        elif fmt == 'LaTeX':
            if col_number == 0:
                out = [' ', '']
            else:
                out = [' & ', '']

        return out

    def get_hline(self, row_number, separator, fmt):
        """
        Return horizontal separator for a given column. Returns an array with the separator for the above and below
        """
        out = ['', '\n']
        if fmt == 'string':
            out = ['', '\n' + separator + '\n']

            if row_number == 0:
                out[0] = out[1]
        if fmt == 'LaTeX':

            out = ['', r' \\ \hline']
            if row_number == 0:
                out[0] = r'\hline'+'\n'
        return out

    def get_intersection(self, col_number, fmt):

        if fmt == 'string':
            separation = ['+', '+']
        elif fmt == 'LaTeX':
            separation = ['&', '&']
        return separation

    def get_TeX_header(self, head_size, alignment):
        alg_str = ['|' for _ in range(head_size)]
        return self._build_header_vlines(alg_str, alignment)


class MNRAS(Style):
    def get_vline(self, col_number, fmt):
        """
        Return vline separator for a given column. Returns an array with the separator for the left and right
        """
        out = ['', '']
        if fmt == 'string':
            out = [' ', '']
            if col_number == 0:
                out = ['', '']
        elif fmt == 'LaTeX':
            if col_number == 0:
                out = [' ', '']
            else:
                out = [' & ', '']

        return out

    def get_hline(self, row_number, separator, fmt):
        """
        Return horizontal separator for a given column. Returns an array with the separator for the above and below
        """
        out = ['', '\n']
        if fmt == 'string':
            if row_number == 0:
                out = ['', '\n' + separator + '\n']
                out[0] = out[1]
        if fmt == 'LaTeX':

            if row_number == 0:
                out = ['', r' \\ \hline']
                out[0] = r'\hline'+'\n'
            else:
                out = ['', r'\\']
        return out

    def get_intersection(self, col_number, fmt):

        if fmt == 'string':
            separation = ['-', '-']
        elif fmt == 'LaTeX':
            separation = ['&', '&']
        return separation

    def get_TeX_header(self, head_size, alignment):
        alg_str = ['|' for _ in range(head_size)]
        return self._build_header_vlines(alg_str, alignment)

class NoLines(Style):
    def get_vline(self, col_number, fmt):
        """
        Return vline separator for a given column. Returns an array with the separator for the left and right
        """
        out = ['', ' ']
        if fmt == 'string':
            out = [' ', ' ']
            if col_number == 0:
                out = ['', '']
        elif fmt == 'LaTeX':
            if col_number == 0:
                out = [' ', '']
            else:
                out = [' & ', '']
        return out

    def get_hline(self, row_number, separator, fmt):
        """
        Return horizontal separator for a given column. Returns an array with the separator for the above and below
        """
        out = ['', '\n']
        if fmt == 'string':
            if row_number == 0:
                out = ['', '\n']
        if fmt == 'LaTeX':
            out = ['', r'\\']
        return out

    def get_intersection(self, col_number, fmt):

        if fmt == 'string':
            separation = ['', ' ']
        elif fmt == 'LaTeX':
            separation = ['&', '&']
        return separation

    def get_TeX_header(self, head_size, alignment):
        alg_str = ['' for _ in range(head_size)]
        return self._build_header_vlines(alg_str, alignment)
