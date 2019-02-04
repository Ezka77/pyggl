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

Well, sometime it come to be quite boring to use the UI from toggl (free
version). So for a long day or many days of work on a single task ... one
command, upload the CSV and done.


NB: there is plenty of nice scripts working with Toggle API, but I like
writing CSV files ... and it works with any other tool who allow you to import
data from Toggl ;-)


## Usage

Get help : `pyggl --help`

Ho BTW it'll append rows to an already existing csv.

## Exemple of configuration file


By default, `pyggl` read default configuration from current directory from a
file name `pyggl.conf`. For exemple:

```INI
[Toggl]
User=MyDummyUser
Email=mydummyemail@mydummy.com
Project=MyDummyProject
Tags=MyDummyTag
Description=A dummy task description

[pyggl]
period_per_day = 8-12,14-18
```

Command line argument take precedence over this file. You can for exemple use
one file per project with these defaults:

```INI
[Toggl]
Email=pinkyandthebrain@acme.labs
Project=Takeover the world !
```
