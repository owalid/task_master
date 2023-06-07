<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/owalid/task_master/assets/28403617/c525087f-a5fd-48ca-ab7b-8f9b61000834">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/owalid/task_master/assets/28403617/17f5466a-c5a5-43e9-8a6c-f8615e278edf">
    <img src="https://github.com/owalid/task_master/assets/28403617/17f5466a-c5a5-43e9-8a6c-f8615e278edf">
  </picture>
</div>


## Description

Basic job control features are the suspending, resuming, or terminating of all processes in the job/process group; more advanced features can be performed by sending signals to the job. Job control is of particular interest in Unix due to its multiprocessing, and should be distinguished from job control generally, which is frequently applied to sequential execution (batch processing).

Our job here was to make a fully-fledged job control daemon like supervisord or systemd.

## Installation

```bash-session
pip install -r requirements.txt
```

## Usage

Start the server:

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

Start the client:

```bash-session
python taskmasterctl.py
```

## Example

Start the server:

```bash-session
python3 taskmaster.py -c config.yaml
```

You can find examples of configuration files in the [`config_file_example`](https://github.com/owalid/task_master/tree/main/config_file_example) folder.

Start the client:

```bash-session
python3 taksmasterctl.py
```