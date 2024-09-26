import argparse
import csv
import requests
import time
from dataclasses import dataclass
from splinter import Browser

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

api = "https://docs.google.com/forms/d/1w1d2qiCerKxjR5uu7gnqRqF9XpYeRvTDPqHbCE4Cftc/formResponse"

NAME = "entry.508902369"
EMAIL = "entry.119277156"
PHONE = "entry.1046234029"
ADDRESS = "entry.214227195"
APARTMENT = "entry.290479075"
REFERENCE = "entry.1698570874"
NCL = "entry.1263551439"
PASSWORD = "entry.508430148"


@dataclass
class Member:
    name: str
    email: str
    phone: str
    address: str
    apartment: str


def main():
    parser = argparse.ArgumentParser(
        prog="ProgramName",
        description="What the program does",
        epilog="Text at the bottom of help",
    )

    parser.add_argument("--real", action="store_true")
    parser.add_argument("--file", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--splinter", action="store_true")
    group.add_argument("--api", action="store_true")

    args = parser.parse_args()

    with open(args.file, newline="") as csvfile:
        request_reader = csv.DictReader(csvfile, delimiter="|")

        for row in request_reader:
            try:
                member = Member(**row)
                if args.splinter:
                    use_splinter(member)
                elif args.api:
                    use_api(member)
            except Exception as e:
                print(f"Could not parse submission. Row was: {row}. {e}")
                input("Press enter to continue or ^C to quit")


def use_splinter(member: Member, for_real: bool = False):
    try:
        b = Browser("firefox")
        b.visit("https://www.nycmesh.net/es/join")

        form_submission = {
            NAME: member.name,
            EMAIL: member.email,
            PHONE: member.phone,
            ADDRESS: member.address,
            APARTMENT: member.apartment,
            REFERENCE: "BAM Data Dump",
            # "entry.1263551439": "I+agree+to+the+Network+Commons+License", # NCL
            # "entry.508430148": "hunter2", # Password
        }

        for k, v in form_submission.items():
            b.find_by_name(k).fill(v)

        b.find_by_name(NCL).click()  # Agree to NCL

        if for_real:
            b.find_by_value("Enviar peticion").click()  # Send it

        time.sleep(3)

        print(f"Submitted via splinter. Member: {member}")
    except Exception as e:
        print(f"Could not submit via splinter. Member: {member}. {e}")


def use_api(member: Member):
    # On the form, the keys here are the names of the field, and I guess
    # they correspond to the expected google forms lads.
    form_submission = {
        NAME: member.name,
        EMAIL: member.email,
        PHONE: member.phone,
        ADDRESS: member.address,
        APARTMENT: member.apartment,
        REFERENCE: "BAM Data Dump",
        NCL: "I+agree+to+the+Network+Commons+License",  # NCL
        PASSWORD: "hunter2",  # Password
    }
    try:
        print(form_submission)
        r = requests.post(api, data=form_submission)
        print(f"Status code: {r.status_code}")
        input("Please check the status code!!!!!!!!!!!!!!!")
        print("Sleeping to make sure you checked the status code.")
        time.sleep(30)
    except Exception as e:
        print(f"Could not submit join form. Submission was {member}. {e}")
        input("Press enter to continue or ^C to quit")


if __name__ == "__main__":
    main()
