# task_master


<div align="center">
<img width="450px" height="450px" src="https://github.com/owalid/task_master/assets/28403617/17f5466a-c5a5-43e9-8a6c-f8615e278edf#gh-light-mode-only">
<img width="450px" height="450px" src="https://github.com/owalid/task_master/assets/28403617/c525087f-a5fd-48ca-ab7b-8f9b61000834#gh-dark-mode-only">
</div>


## Installation

```bash-session
pip install -r requirements.txt
```

## Usage

Start the "server":

```
python taskmaster.py
usage: taskmaster.py [-h] [-c CONF] [-k] [-df] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  Path of your configuration file
  -k, --kill            Kill taskmaster
  -df, --default        Use default value of all the questions asked by the program
  -d, --deamonize       Deamonize
```

Start the "client":

```bash-session
python taskmasterctl.py
```

## Example

```bash-session
python3 taskmaster.py -c config.yaml
```

```bash-session
python3 taksmasterctl.py
```