import requests
from twilio.rest import Client
import sys
from pathlib import Path
from datetime import datetime

ICERT_URL = "https://icert.doleta.gov/"
OLD_TEXT_FILENAME = "old_icert_text.txt"

def check_icert() -> int:

    now = datetime.now()
    print(f"Checking {ICERT_URL} at {now}")
    # Step 1: GET the icert portal
    icert_response = requests.get(ICERT_URL)

    if icert_response.status_code != 200:
        print(f"Error: Failed to GET {ICERT_URL}")
        return 1
    
    # We got it, so let's clean up the text
    icert_text = icert_response.text \
        .replace('\n', '') \
        .replace('\t', '') \
        .lower()

    # If there is an old file, read and compare it.
    old_text_path = Path(OLD_TEXT_FILENAME)
    if old_text_path.is_file():
        old_text = None
        with open(OLD_TEXT_FILENAME, 'r', encoding='utf-8') as f:
            old_text = f.read()

        if icert_text != old_text:
            # Text has changed! Alert People!
            print("The text has changed:\n")
            print(icert_response.text)

            # TODO: Send Twilio SMS
        else:
            print("no change.")

    # Write the content as our new file.
    with open(OLD_TEXT_FILENAME, 'w', encoding='utf-8') as f:
        f.write(icert_text)

    return 0


if __name__ == "__main__":
    sys.exit(check_icert())