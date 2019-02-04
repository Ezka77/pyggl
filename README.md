# Toggl for lazy people

... or in need of a time travel machine.

## Installation

Requirements:
- click

Works with python 3.7 ... not tested below that version

Install from source

```
pip install -e .
```

Or build the package:
```
python setup.py bdist_wheel sdist
```

and install:

```
pip install dist/pyggl-0.1-py3-none-any.whl
```


## WTF of this script ?

Well, sometime it come to be quite boring to duplicate and modify time on
toggl (free version). So for a long day or many days of work on a single task
... one command, upload the CSV and done.


## Usage

Get help : `pyggl --help`

Ho BTW it'll append rows to an already existing csv.
