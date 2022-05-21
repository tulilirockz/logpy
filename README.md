Bookitty
=========

Simple and quick logging for user applications and scripts.

Can be used when, for example, you schedule a very lenghy task and you want to know whether or not it was successful or not, running it may help!

```sh
very_lengthy_task && bookitty "Ran TASK successfully" -l INFO -c TASK  || bookitty "Failed running TASK" -l CRITICAL -c TASK
```

- Compatible with Linux (tested on Ubuntu) and Windows (not tested yet.)

## Configuration
Configurable through its "config-file" argument, by default the conf. file will be at:
- Windows: C:\\Users\\%USERNAME%\\.bookitty\\bookitty.conf
- Linux: $XDG_CONFIG_HOME/bookitty/bookitty.conf

## Dependencies
Just the Python3 std libraries and that's it!

## Installation
Move it to anywhere on your $PATH variable or run `chmod +x ./install.sh && ./install.sh` on linux
