"""gpgimporter
Import and update all keys from any keyserver.

Just a very simple Python tool, without any fancy code-design bla-bla.
"""

import argparse
import datetime
import subprocess
import sys
import gnupg


def cleanup_all_keys():
    print("Cleaning up expired and duplicate keys..")

    now = datetime.datetime.now()
    newest_by_uid = {}
    keys_to_delete = []

    for key in gpg.list_keys():
        fingerprint = key["fingerprint"]
        uid = key["uids"][0]  # or another UID selection strategy

        # ---- Expiration check ----
        expires = key.get("expires")
        if expires:
            try:
                if datetime.datetime.fromtimestamp(int(expires)) < now:
                    print(f"Deleting expired key of '{uid}'")
                    keys_to_delete.append(fingerprint)
                    continue  # don't consider expired key for duplicate logic
            except (ValueError, TypeError):
                pass

        # ---- Duplicate handling ----
        created = int(key["date"])

        existing = newest_by_uid.get(uid)
        if existing is None:
            newest_by_uid[uid] = (created, fingerprint)
        else:
            existing_created, existing_fp = existing
            print(f"Deleting duplicate key of '{uid}'")

            if created > existing_created:
                # Current key is newer → delete previous
                keys_to_delete.append(existing_fp)
                newest_by_uid[uid] = (created, fingerprint)
            else:
                # Existing key is newer → delete current
                keys_to_delete.append(fingerprint)

    # Delete everything at the end
    for fingerprint in keys_to_delete:
        gpg.delete_keys(fingerprint)

parser = argparse.ArgumentParser(
    prog="gpgimporter",
    description="Import and update all keys from any keyserver",
    epilog="Really simple and stupid",
)

parser.add_argument(
    "-k",
    "--keyserver",
    help="Keyserver hostname without https:// or hkps:// prefix.",
    required=True,
)
parser.add_argument("-l", "--lookup", help="Any string to filter the GPG list by.")
parser.add_argument(
    "-t",
    "--trust-level",
    help="Trust level to set for the imported keys ('TRUST_EXPIRED', 'TRUST_UNDEFINED', 'TRUST_NEVER', 'TRUST_MARGINAL', 'TRUST_FULLY' or 'TRUST_ULTIMATE').",
    default="TRUST_FULLY",
)
parser.add_argument(
    "-s",
    "--sign",
    help="Sign imported keys with your default key.",
    action="store_true",
)
parser.add_argument(
    "-r",
    "--refresh",
    help="Only refresh and cleanup existing keys.",
    action="store_true",
)

options = parser.parse_args()
gpg = gnupg.GPG()

if options.refresh:
    cleanup_all_keys()
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
    sys.exit(0)

if options.lookup is None:
    print("--lookup must be provided")
    sys.exit(1)

search_results = gpg.search_keys(
    options.lookup, keyserver=f"hkps://{options.keyserver}"
)
key_ids = [d["keyid"] for d in search_results]

if len(search_results) != len(key_ids):
    print("Something went wrong with importing the keys from your key server!")

print(f"Number of keys: {len(key_ids)}")
print("Importing keys.. (might take some time)")
imported_keys = gpg.recv_keys(f"hkps://{options.keyserver}", *key_ids)
print(f"Number of imported keys: {imported_keys.count}")

gpg.trust_keys(imported_keys.fingerprints, options.trust_level)

if not options.sign:
    sys.exit(0)

for f in imported_keys.fingerprints:
    try:
        subprocess.run(f"gpg --quick-sign-key '{f}'", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        print(f"Deleting the key '{f}'")
        gpg.delete_keys(f)

cleanup_all_keys()
