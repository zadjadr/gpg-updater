# gpg-updater

Import and update all keys from any keyserver.

Just a very simple Python tool, without any fancy code-design bla-bla.

## Usage

Either use `pipenv` or `pip` to install the dependencies.

```bash
# Install via `pip`
python -m pip install -r requirements.txt

python gpgimporter.py -h

usage: gpgimporter [-h] -k KEYSERVER [-l LOOKUP] [-t TRUST_LEVEL] [-s] [-r]

Import and update all keys from any keyserver

options:
  -h, --help            show this help message and exit
  -k KEYSERVER, --keyserver KEYSERVER
                        Keyserver hostname without https:// or hkps:// prefix.
  -l LOOKUP, --lookup LOOKUP
                        Any string to filter the GPG list by.
  -t TRUST_LEVEL, --trust-level TRUST_LEVEL
                        Trust level to set for the imported keys ('TRUST_EXPIRED', 'TRUST_UNDEFINED', 'TRUST_NEVER', 'TRUST_MARGINAL',
                        'TRUST_FULLY' or 'TRUST_ULTIMATE').
  -s, --sign            Sign imported keys with your default key.
  -r, --refresh         Only refresh and cleanup existing keys.

Really simple and stupid
```

```bash
# Install via pipenv
python -m pip install pipenv
pipenv install
pipenv run python gpgimporter.py -h

usage: gpgimporter [-h] -k KEYSERVER [-l LOOKUP] [-t TRUST_LEVEL] [-s] [-r]

Import and update all keys from any keyserver

options:
  -h, --help            show this help message and exit
  -k KEYSERVER, --keyserver KEYSERVER
                        Keyserver hostname without https:// or hkps:// prefix.
  -l LOOKUP, --lookup LOOKUP
                        Any string to filter the GPG list by.
  -t TRUST_LEVEL, --trust-level TRUST_LEVEL
                        Trust level to set for the imported keys ('TRUST_EXPIRED', 'TRUST_UNDEFINED', 'TRUST_NEVER', 'TRUST_MARGINAL',
                        'TRUST_FULLY' or 'TRUST_ULTIMATE').
  -s, --sign            Sign imported keys with your default key.
  -r, --refresh         Only refresh and cleanup existing keys.

Really simple and stupid
```
