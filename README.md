The goal of this project is to allow an easy interface to create Tables that are not only printed nicely in the terminal, but can
also be easily exported to LaTeX code.


# How to Install




# How to use

from tabletexifier import Table

x = Table(['Name', 'b','c','d','e']) 
x.add_row(['first',1,4,6,7])
x.add_row(['first',1,4,6,7])
print(x.build_latex())