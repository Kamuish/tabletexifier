The goal of this project is to allow an easy interface to create Tables that are not only printed nicely in the terminal, but can
also be easily exported to LaTeX code.


# How to Install




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