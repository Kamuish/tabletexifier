"""Define the cells of the Tables


Returns:
    _type_: _description_
"""


class Cell:
    def __init__(self, content, origin, n_rows=1, n_cols=1, is_blank=False):
        # Starting coordinates, in the upper-left corner of the cell
        self.origin = origin
        self.content = content
        self.dimension = [n_rows, n_cols]

        self.next_col = None
        self.previous_col = None
        self.next_row = None
        self.previous_row = None
        self.is_blank = is_blank
        self._decimal_places = None
        # number of cells

        self._design_properties = {
            "color": None,
            "fmt_type": "normal",
            "left_border": False,
            "right_border": False,
        }
        self._responsible_for_borders = False

    def update_size(self, nrows=None, ncols=None):
        if nrows is not None:
            self.dimension[0] = nrows
        if ncols is not None:
            self.dimension[1] = ncols

    def set_decimal_places(self, value):
        self._decimal_places = value

    def get_content(self, fmt: str = "text") -> str:
        if fmt == "text":
            return self.generate_text()
        return self.generate_LaTeX()

    @property
    def row_number(self) -> int:
        return self.origin[0]

    @property
    def col_number(self) -> int:
        return self.origin[1]

    @property
    def is_multirow(self) -> bool:
        return self.dimension[0] > 1

    @property
    def is_multicol(self) -> bool:
        return self.dimension[1] > 1

    def generate_text(self) -> str:
        if self.is_blank:
            return ""
        val = self.content
        if isinstance(val, (float, int)) and self._decimal_places is not None:
            return "{:.{}f}".format(val, self._decimal_places)
        return str(val)

    def generate_LaTeX(self) -> str:
        """Generate the LaTeX representation of this cell

        Returns:
            str: _description_
        """

        if (
            self.is_blank
            and self.previous_row is not None
            and self.previous_row.is_multirow
            and self.previous_row.is_multicol
        ):
            return r"\multicolumn{" + str(self.previous_row.dimension[1]) + r"}{c}{}"

        if self.is_blank:
            return ""

        val = self.content

        if isinstance(val, float):
            val = "{:.{}f}".format(val, self._decimal_places)

        if self._design_properties["color"] is not None:
            val = "\textcolor{}{}".format(self._design_properties["color"], val)

        if self.is_multirow:
            val = r"\multirow{" + str(self.dimension[0]) + r"}{*}{" + f"{val}" + "}"

        if self.is_multicol:
            val = r"\multicolumn{" + str(self.dimension[1]) + r"}{c}{" + f"{val}" + "}"

        return str(val)

    def set_property(self, param, new_value):
        self._design_properties[param] = new_value

    def get_property(self, param):
        pass

    def update_origin(self, new_origin):
        self.origin = new_origin

    def __repr__(self) -> str:
        return f"Cell with {self.content=}; {self.is_multicol=}, {self.is_multirow=}"


if __name__ == "__main__":
    cell = Cell(ID=0, origin=[1, 1], n_cols=3, n_rows=3)
    print(cell)
