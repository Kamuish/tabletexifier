# Goal of the project 

Provide an easy interface to create Tables that are not only printed nicely in the terminal, but can
also be easily exported to LaTeX code. It is also desired to easily create tables in the format required by multiple scientific journals.


# How to Install

```
pip install tabletexifier
```

# How to use

```
>>> from tabletexifier import Table
>>> x = Table(['Name', 'b','c','d','e'], table_style = 'A')  
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
 | second | 1.0000 | 4.0000 | 6.0000 | 7.0000 |
 ----------------------------------------------
 ```

 The columns also allow the data to be tuples or lists. However, the decimal places do not apply to them:
 
 ```
>>> x.add_row(['third',[1,1,1], [], (1,1,1),()])
 ----------------------------------------------------
 | Name   | b         | c      | d         | e      |
 +--------+-----------+--------+-----------+--------+
 | first  | 1.0000    | 4.0000 | 6.0000    | 7.0000 |
 +--------+-----------+--------+-----------+--------+
 | second | 1.0000    | 4.0000 | 6.0000    | 7.0000 |
 +--------+-----------+--------+-----------+--------+
 | third  | [1, 1, 1] | []     | (1, 1, 1) | ()     |
 ----------------------------------------------------
  ```

To only have a cross patern of lines:

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

There is also the option to have all lines in the table (the default option):

 ```
>>> x.set_design_property("lines", 'A')
 --------------------------
 | Name   | b | c | d | e |
 +--------+---+---+---+---+
 | first  | 1 | 4 | 6 | 7 |
 +--------+---+---+---+---+
 | second | 1 | 4 | 6 | 7 |
 --------------------------
 ```

 Or to use the format from different scientific journals:

  ```
>>> x.set_design_property("lines", 'MNRAS') # monthly notices of the royal astronomical society
 --------------
 Name   b c d e
 --------------
 first  1 4 6 7
 second 1 4 6 7
 ```

To store the data to file:

```
>>> x.write_to_file("<path>_<to>_<file>", mode='a', write_table = True, write_LaTeX=False)
    # mode is the normal file.write mode
    # write_table to write the ASCII table
    # write_LaTeX to write the latex code to build the table
```


#  Roadmap for 1.0

  - Add more common LaTex Tables styles:
    - [ ] A&A (table and longtable)
    - [ ] APJ
  - Functionalities:
    - [x] Delete rows and columns 
    - [x] Easier way to change alignement of Latex columns
    - [ ] Allow to add extra vertical and horizontal lines
  - QoL:
    - [ ] Testing the multiple features
    - [ ] Continuous integration
    - [ ] Proper documentation

# Development

Create a virtual environment and run
```
pip install -r requirements_dev.txt
```
in order to install development dependencies.


In order to run the tests and see coverage reports, use
```
pytest --cov=. test --cov-report html
```

