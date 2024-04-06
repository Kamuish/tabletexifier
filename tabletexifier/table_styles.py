from operator import add
from typing import Tuple


class Style:
    def __init__(self, vline_locs=None, hline_locs=None, header=None):
        self.vline_locs = vline_locs if vline_locs is not None else []
        self.hline_locs = hline_locs if hline_locs is not None else []
        self.header = {i: "" for i in ["text", "LaTeX"]} if header is None else header

        self.nrows = None
        self.ncols = None
        self.table_properties = {"caption": "", "label": "", "column_alignement": "c"}

        self.extra_vline = []
        self.extra_hline = []

    def add_vline(self, loc):
        self.extra_vline.append(loc)

    def add_hline(self, loc):
        self.extra_hline.append(loc)

    def set_LaTeX_property(self, prop, value):
        self.table_properties[prop] = value

    def set_size(self, rows, cols):
        self.ncols = cols
        self.nrows = rows

    def get_hline_positions(self):
        return (*self.hline_locs, *self.extra_hline)

    def get_vline_positions(self):
        return (*self.vline_locs, *self.extra_vline)

    def get_col_separation(self, row_number, col_number, cell, fmt):
        if fmt == "text":
            out = " "
            if col_number in self.get_vline_positions():
                if (
                    cell.is_blank
                    and cell.previous_col is not None
                    and cell.previous_col.is_multicol
                ):
                    out = " "
                else:
                    out = "|"

        elif fmt == "LaTeX":
            if col_number == self.ncols:
                out = r"\\"
                if row_number + 1 in self.get_hline_positions():
                    counts = self.get_hline_positions().count(row_number + 1)
                    for _ in range(counts):
                        out += r" \hline"

            elif col_number != 0 and not (
                cell.is_blank and cell.previous_col.is_multicol
            ):
                out = "&"
            else:
                out = ""
        return out

    def check_if_duplicate_row(self, row_number) -> Tuple[bool, int]:
        res = row_number in self.get_hline_positions()
        n = self.get_hline_positions().count(row_number)
        return res, n

    def get_row_separation(self, row_number, col_number, col_size, cell, fmt):
        out = ""
        if fmt == "text":
            if row_number in self.get_hline_positions():
                new_row = ""
                if col_number in self.get_vline_positions():
                    new_row += "+"
                    if (
                        cell.is_blank
                        and cell.previous_row is not None
                        and cell.previous_row.is_multirow
                        and row_number
                        != self.nrows  # Ensures that things don't break on the last row
                    ):
                        new_row += " " * col_size
                    else:
                        new_row += "-" * (col_size)
                    if col_number == self.ncols - 1:
                        # Get the last vertical line
                        new_row += "+"

                else:
                    new_row += "-" * (col_size + 1)
                out += new_row
            else:
                out = "" * (col_size + 2)
        else:
            out = ""
        return out

    def _build_header_vlines(self, v_fmt, alignment):
        return list(map(add, v_fmt, alignment)) + [v_fmt[-1]]

    def get_TeX_header(self) -> str:
        cols = ""

        for index in range(self.ncols):
            if index in self.get_vline_positions():
                cols += "|"
            cols += self.table_properties["column_alignement"]

        base_header = [
            r"\begin{table}[H]",
            r"\caption{" + self.table_properties["caption"] + "}",
            r"\label{" + self.table_properties["label"] + "}",
            r"\centering",
            r"\begin{tabular}{" + cols + "}",
        ]
        return "\n".join(base_header)

    def get_TeX_footer(self) -> str:
        return r"\end{tabular}" + "\n" + r"\end{table}"


class Tlines(Style):
    def __init__(self):
        super().__init__(vline_locs=(1,), hline_locs=(1,))


class Alines(Style):
    def set_size(self, rows, cols):
        super().set_size(rows, cols)
        self.hline_locs = list(range(rows + 1))
        self.vline_locs = list(range(cols + 1))


class AA(Style):
    def set_size(self, rows, cols):
        super().set_size(rows, cols)
        self.hline_locs = (0, 0, 1, rows)

    def get_TeX_header(self) -> str:
        head = super().get_TeX_header()
        head += "\hline \hline"
        return head


class MNRAS(Style):
    def __init__(self):
        super().__init__(
            hline_locs=(
                0,
                1,
            )
        )


class NoLines(Style): ...
