Loggy
=========

Simple and quick logging for user applications and scripts.

Can be used when, for example, you schedule a very lenghy task and you want to know whether or not it was successful or not, running it may help!

```sh
very_lengthy_task && loggy "Ran TASK successfully" -l INFO -c TASK  || loggy "Failed running TASK" -l CRITICAL -c TASK
```

- Compatible with Linux (tested on Ubuntu) and Windows (not tested yet.)

## Configuration

Configurable through its "config-file" argument, by default the conf. file will be at:
- Windows: %APPDATA%\\Loggy\\loggy.conf
- Linux: $XDG_CONFIG_HOME/bookitty/bookitty.conf

## Installation

Install it though poetry or copy it to a folder in your $PATH
