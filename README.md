# Python & UV Commands Cheat Sheet

## Python Prompt

``` python
import shutil
print(shutil.which("uv"))
exit()
```

-   Enter on python mode\
-   Check uv installation path\
-   To exit python prompt

------------------------------------------------------------------------

## UV Commands

### Check UV Version

``` bash
uv --version
```

-   Check uv version

### Install UV

``` bash
pip install uv
```

-   Install uv

### Upgrade UV

``` bash
uv self update
```

-   Upgrade uv version

### Initialize Project

``` bash
uv init llm-ecomm-assistant
```

------------------------------------------------------------------------

## Package Management

### List Installed Packages

``` bash
uv pip list
```

-   List of installed python packages

### List Available Python Versions

``` bash
uv python list
```

-   List of available python versions

### Install Specific Python Version

``` bash
uv python install cpython-3.11.13-windows-x86_64-none
```

-   Install specific Python version

### Create Virtual Environment

``` bash
uv venv <venv> --python 3.10.18
```

-   Create virtual environment

### Activate Virtual Environment

``` bash
<venv>\Scripts\activate
```

-   Activate created virtual environment

### Install Requirements

``` bash
uv pip install -r requirements.txt
```

### Install dotenv

``` bash
uv pip install python-dotenv
```
