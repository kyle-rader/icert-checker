import requests
from twilio.rest import Client
import sys
from pathlib import Path
from datetime import datetime

from_phone = sys.argv[1]
account_sid = sys.argv[2]
auth_token = sys.argv[3]
to_phones = sys.argv[4:]

ICERT_URL = "https://icert.doleta.gov/"
OLD_TEXT_FILENAME = "old_icert_text.txt"

def send_alert(to_phone: str):
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                    body=f"The contents of \n{ICERT_URL}\nhas changed!",
                    from_=from_phone,
                    to=to_phone
                )
    
    print(f"Sent message to {to_phone}\n{message.sid}")


def check_icert() -> int:

    now = datetime.now()
    print(f"Checking {ICERT_URL} at {now}")
    # Step 1: GET the icert portal
    icert_response = requests.get(ICERT_URL)

    if icert_response.status_code != 200:
        print(f"Warning: Failed to GET {ICERT_URL} - status code {icert_response.status_code}")
    
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
            for phone in to_phones:
                send_alert(phone)
        else:
            print("no change.")

    # Write the content as our new file.
    with open(OLD_TEXT_FILENAME, 'w', encoding='utf-8') as f:
        f.write(icert_text)

    return 0


if __name__ == "__main__":
    sys.exit(check_icert())