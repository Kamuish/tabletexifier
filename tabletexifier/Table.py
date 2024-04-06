from typing import List
from tabletexifier.table_styles import Tlines, Alines, MNRAS, NoLines, AA
from .Cell import Cell
from .exceptions import ColumnDoesNotExist, RowDoesNotExist


class Table:
    def __init__(
        self,
        header,
        table_style="A&A",
    ):
        self._style_map = {
            "T": Tlines,
            "A": Alines,
            "MNRAS": MNRAS,
            "NoLines": NoLines,
            "A&A": AA,
        }

        self._table_style = self._style_map[table_style]()

        self._largest_entry = [len(str(head)) for head in header]

        # Number of decimal places in the numbers
        self._decimal_places = None

        self._tableCells = []
        self.nrows = 0
        self.ncols = len(header)
        self.add_row(header)

    def add_table_caption(self, caption: str):
        self._table_style.set_LaTeX_property("caption", caption)

    def add_table_label(self, label: str):
        self._table_style.set_LaTeX_property("label", label)

    def add_vline(self, loc):
        self._table_style.add_vline(loc)

    def add_hline(self, loc):
        self._table_style.add_hline(loc)

    def add_row(self, row):
        """
        Adds a new row to the table; Assumes that the order is the same as the one given in the header
        """
        previous = None
        for index, val in enumerate(row):
            new_cell = Cell(content=val, origin=[self.nrows, index])
            new_cell.previous_col = previous
            self._tableCells.append(new_cell)

        newly_added_cells = self._tableCells[-len(row) :]
        # Make the links for the next column
        for index, cell in enumerate(
            newly_added_cells[:-1]
        ):  # the last col does not have a "next_col"
            cell.next_col = newly_added_cells[index + 1]

        if self.nrows > 0:
            # Make the links for the previous row
            prev_row = self.get_line(self.nrows - 1)
            for upper, lower in zip(prev_row, newly_added_cells):
                upper.next_row = lower
                lower.previous_row = upper

        self.nrows += 1

    def get_line(self, line_number) -> List[Cell]:
        """
        Return an entire line; The line number is zero-indexed

        Parameters
        ===============
        line_number: int
            Line number to print; Zero-indexed; Does not count the header!!!
        """
        line = []
        first_cell = self._tableCells[0]
        while first_cell.row_number != line_number:
            first_cell = first_cell.next_row
            if first_cell is None:
                raise RowDoesNotExist(f"Row {line_number} does not exist")

        while first_cell is not None:
            line.append(first_cell)
            first_cell = first_cell.next_col
        return line

    def get_column(self, column_number: int) -> List[Cell]:
        """Get a column through a zero-indexed index

        Args:
            column_number (int): Column number

        Raises:
            ColumnDoesNotExist: If the column does not exist

        Returns:
            List[Cell]: List with Cell objects
        """
        col = []

        first_cell = self._tableCells[0]
        while first_cell.col_number != column_number:
            first_cell = first_cell.next_col
            if first_cell is None:
                raise ColumnDoesNotExist(f"Column {column_number} does not exist")

        while first_cell is not None:
            col.append(first_cell)
            first_cell = first_cell.next_row
        return col

    def compute_max_text_size_of_cols(self) -> List[int]:
        """Find the maximum text size that we will need for each column to esure formatted outputs in the terminal

        Returns:
            List[int]: List with max size of each column
        """
        text_sizes = []
        for col_number in range(self.N_columns):
            col = self.get_column(col_number)
            col_size = [len(i.generate_text()) for i in col]
            max_size = max(col_size)
            if not max_size % 2 == 0:
                max_size += 1

            max_size += 2
            text_sizes.append(max_size)
        return text_sizes

    def get_pretty_print(self, ignore_cols, fmt="text") -> List[str]:
        """Generate the textual representation of the table, under a given format

        Args:
            ignore_cols (_type_): _description_
            fmt (str, optional): Which format to use, between text and LaTeX. Defaults to "text".

        Returns:
            List[str]: _description_
        """
        text_sizes = self.compute_max_text_size_of_cols()
        lines = []
        self._table_style.set_size(rows=self.nrows, cols=self.N_columns)
        for row_index in range(self.nrows):
            row = [i.generate_text() for i in self.get_line(row_index)]

            line = ""
            row_separator = ""
            for col_index, col_value in enumerate(row):
                max_size = text_sizes[col_index]
                padding = " " * (int((max_size - len(col_value)) / 2))

                entry = f"{padding}{col_value}{padding}"
                col_sep = self._table_style.get_col_separation(
                    row_number=row_index, col_number=col_index, fmt=fmt
                )
                row_sep = self._table_style.get_row_separation(
                    row_number=row_index,
                    col_number=col_index,
                    col_size=max_size,
                    fmt=fmt,
                )

                line = f"{line}{col_sep}{entry}"
                row_separator = f"{row_separator}{row_sep}"
            col_sep = self._table_style.get_col_separation(
                row_number=row_index, col_number=self.ncols, fmt=fmt
            )
            line = f"{line}{col_sep}"
            dup, n_times = self._table_style.check_if_duplicate_row(row_index)
            if not dup:
                n_times = 1
            for _ in range(n_times):
                lines.append(row_separator)

            lines.append(line)
        # grab the last line of the table
        row_separator = ""
        for col_index, col_value in enumerate(row):
            row_sep = self._table_style.get_row_separation(
                row_number=self.nrows,
                col_number=col_index,
                col_size=max_size,
                fmt=fmt,
            )
            row_separator = f"{row_separator}{row_sep}"
        lines.append(row_separator)
        return "\n".join((i for i in lines if i))

    def build_latex(self, ignore_cols=None) -> List[str]:
        """Generate the LaTeX representation of the table

        Args:
            ignore_cols (_type_, optional): _description_. Defaults to None.

        Returns:
            List[str]: _description_
        """
        main_text = self.get_pretty_print(False, "LaTeX")
        head = self._table_style.get_TeX_header()
        foot = self._table_style.get_TeX_footer()
        return f"\n{head}\n{main_text}\n{foot}"

    def set_decimal_places(self, value: int):
        if value < 0:
            raise ValueError(
                f"The number of decimal places must be positive. Got {value}"
            )

        self._decimal_places = value
        for c in self._tableCells:
            c.set_decimal_places(value)

    def write_to_file(
        self, path, mode="a", write_table=True, write_LaTeX=False, ignore_cols=None
    ):
        with open(path, mode=mode) as file:
            if write_table:
                lines = self.get_pretty_print(fmt="string", ignore_cols=ignore_cols)
                file.write("".join(lines))
            if write_LaTeX:
                if write_table:
                    file.write("\n")
                lines = self.build_latex()
                file.write(lines)

    @property
    def N_columns(self) -> int:
        """Return the number of columns in the table"""
        return len(self.get_line(0))

    @property
    def N_lines(self) -> int:
        """Return the number of lines in the table"""
        return self.nrows

    def __str__(self):
        return "".join(self.get_pretty_print(fmt="text", ignore_cols=[]))
