"""gpgimporter
Import and update all keys from any keyserver.

Just a very simple Python tool, without any fancy code-design bla-bla.
"""

import argparse
import subprocess
import re
import sys

import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(
    prog="gpgimporter",
    description="Import and update all keys from any keyserver",
    epilog="Really simple and stupid",
)


parser.add_argument(
    "-k", "--keyserver", help="Keyserver hostname without https:// or hkps:// prefix."
)
parser.add_argument("-l", "--lookup", help="Any string to filter the GPG list by.")
parser.add_argument("-r", "--refresh", action="store_true")

options = parser.parse_args()

if options.keyserver is None:
    print("--keyserver must be provided")
    sys.exit(1)

if options.refresh:
    subprocess.run(
        [
            "gpg",
            "--batch",
            "--keyserver",
            f"hkps://{options.keyserver}",
            "--refresh-keys",
        ],
        check=True,
    )
    list_expired_keys = subprocess.run(
        "gpg",
        "--list-keys",
        "|",
        "grep -1 pub",
        "|",
        "sed 'N;s/\n/ /'",
        "|",
        "awk '/^pub.* \[expired\: / {id=$7; sub(/^.*\//, \"\", id); print id}'",
        "|",
        "fmt -w 999",
    )
    list_revoked_keys = subprocess.run(
        "gpg",
        "--list-keys",
        "|",
        "grep -1 pub",
        "|",
        "sed 'N;s/\n/ /'",
        "|",
        "awk '/^pub.* \[revoked\: / {id=$7; sub(/^.*\//, \"\", id); print id}'",
        "|",
        "fmt -w 999",
    )
    sys.exit(0)

if options.lookup is None:
    print("--lookup must be provided")
    sys.exit(1)

lookup_url = f"/pks/lookup?search={options.lookup}&fingerprint=on&op=index"
r = requests.get(f"https://{options.keyserver}{lookup_url}", timeout=5)

soup = BeautifulSoup(r.text)

all_keys = ""
all_fingerprints = []
num_keys = 0

gpg_sha_regex = re.compile(
    r"(?P<hash>\b[0-9a-fA-F]{8}\b).*Fingerprint=(?P<fingerprint>\b[0-9a-fA-F ]+\b)",
    re.DOTALL,
)

for link in soup.find_all("pre"):
    m = re.search(gpg_sha_regex, link.text)
    try:
        all_keys += m.group("hash") + " "
        all_fingerprints.append(m.group("fingerprint"))
        num_keys += 1
    except AttributeError:
        print(f'warn: could not find a key in this line: "{link.text.strip()}"')

print(f"Number of keys: {num_keys}")

subprocess.run(
    f"gpg --batch --keyserver hkps://{options.keyserver} --receive-keys {all_keys}",
    shell=True,
    check=True,
)

for f in all_fingerprints:
    try:
        subprocess.run(f"gpg --quick-sign-key '{f}'", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(e.returncode)
