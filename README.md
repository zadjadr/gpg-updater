# gpg-updater

Import and update all keys from any keyserver.

Just a very simple Python tool, without any fancy code-design bla-bla.

## Usage

Either use `pipenv` or `pip` to install the dependencies.

```bash
# Install via `pip`
python -m pip install -r requirements.txt

python gpgimporter.py -h

usage: gpgimporter [-h] [-k KEYSERVER] [-l LOOKUP] [-r]

Import and update all keys from any keyserver

options:
  -h, --help            show this help message and exit
  -k KEYSERVER, --keyserver KEYSERVER
                        Keyserver hostname without https:// or hkps:// prefix.
  -l LOOKUP, --lookup LOOKUP
                        Any string to filter the GPG list by.
  -r, --refresh

Really simple and stupid
```

```bash
# Install via pipenv
python -m pip install pipenv
pipenv install
pipenv run python gpgimporter.py -h

usage: gpgimporter [-h] [-k KEYSERVER] [-l LOOKUP] [-r]

Import and update all keys from any keyserver

options:
  -h, --help            show this help message and exit
  -k KEYSERVER, --keyserver KEYSERVER
                        Keyserver hostname without https:// or hkps:// prefix.
  -l LOOKUP, --lookup LOOKUP
                        Any string to filter the GPG list by.
  -r, --refresh

Really simple and stupid
```
