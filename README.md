# Goal of the project 

Provide an easy interface to create Tables that are not only printed nicely in the terminal, but can
also be easily exported to LaTeX code. It is also desired to easily create tables in the format required by multiple scientific journals.

Check the docs in here: https://tabletexifier.readthedocs.io/en/latest/


# How to Install

```
pip install tabletexifier
```

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

