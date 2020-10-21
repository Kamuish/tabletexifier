The goal of this project is to allow an easy interface to create Tables that are not only printed nicely in the terminal, but can
also be easily exported to LaTeX code.


# How to Install
```
pip install tabletexifier
```

# How to use
```

>>> from tabletexifier import Table
>>> x = Table(['Name', 'b','c','d','e']) 
>>> x.add_row(['first',1,4,6,7])
>>> x.add_row(['second',1,4,6,7])
```

By printing the table, we have

```
>>> print(x)

 --------------------------
 | Name   | b | c | d | e |
 +--------+---+---+---+---+
 | first  | 1 | 4 | 6 | 7 |
 +--------+---+---+---+---+
 | second | 1 | 4 | 6 | 7 |
 --------------------------
 ```

 It can be converted to Latex by 

 ```
 >>> print(x.build_latex())

\begin{table}
\caption{\label{Tab:}}
\begin{tabular}{|l|l|l|l|l|}
\hline Name   & b & c & d & e \\ \hline
 first  & 1 & 4 & 6 & 7 \\ \hline
 second & 1 & 4 & 6 & 7 \\ \hline
\end{tabular}
\end{table}
 ```

It is also possible to set the number of decimal places in the numerical entries:
 ```
>>> x.set_decimal_places(4)
>>> print(x)

 ----------------------------------------------
 | Name   | b      | c      | d      | e      |
 +--------+--------+--------+--------+--------+
 | first  | 1.0000 | 4.0000 | 6.0000 | 7.0000 |
 +--------+--------+--------+--------+--------+
 | second | 1.1331 | 4.0000 | 6.0000 | 7.1410 |
 ----------------------------------------------
 ```

To build a table with lestt vertical and/or vertical lines: 
 ```
>>> x.set_design_property("lines", 'T')
 ```

will update both the ASCII table and the Latex one:

```
>>> print(x)

  Name   | b c d e
 --------+--------
  first  | 1 4 6 7
  second | 1 4 6 7

>>> print(x.build_latex())
\begin{table}
\caption{\label{Tab:}}
\begin{tabular}{l|llll}
 Name   & b & c & d & e \\ \hline
 first  & 1 & 4 & 6 & 7 \\ 
 second & 1 & 4 & 6 & 7 \\ 
\end{tabular}
\end{table}
```

To store the data to file:
```
>>> x.write_to_file("<path>_<to>_<file>", mode='a', write_table = True, write_LaTeX=False)
    # mode is the normal file.write mode
    # write_table to write the ASCII table
    # write_LaTeX to write the latex code to build the table
```


 # ToDo list 
  - [ ] Add proper docs for missing functionalities (e.g. change alignement of columns or the vertical lines)
  - [ ] Write tests for the functions 	
  