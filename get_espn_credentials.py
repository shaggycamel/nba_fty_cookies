"""
ESPN Fantasy Credential Extractor
-----------------------------------
Reads your browser's cookies for espn.com and prints the SWID and
espn_s2 values needed to connect your ESPN Fantasy league.

This only reads cookies already stored locally in your own browser.
Nothing is sent anywhere automatically - copy the printed values and
send them back however you were asked to.

Requirements:
    pip install browser-cookie3

Usage:
    python get_espn_credentials.py
"""

import sys

try:
    import browser_cookie3
except ImportError:
    print("Missing dependency. Install it first with:\n\n    pip install browser-cookie3\n")
    sys.exit(1)


BROWSERS = [
    ("Chrome", browser_cookie3.chrome),
    ("Firefox", browser_cookie3.firefox),
    ("Edge", browser_cookie3.edge),
    ("Brave", getattr(browser_cookie3, "brave", None)),
    ("Safari", getattr(browser_cookie3, "safari", None)),
]


def find_espn_cookies():
    for name, loader in BROWSERS:
        if loader is None:
            continue
        try:
            cj = loader(domain_name="espn.com")
        except Exception:
            continue

        swid = None
        espn_s2 = None
        for cookie in cj:
            if cookie.name == "SWID":
                swid = cookie.value
            elif cookie.name == "espn_s2":
                espn_s2 = cookie.value

        if swid and espn_s2:
            return name, swid, espn_s2

    return None, None, None


def main():
    print("Looking for ESPN Fantasy login cookies in your browsers...\n")
    browser_name, swid, espn_s2 = find_espn_cookies()

    if not swid or not espn_s2:
        print(
            "Couldn't find ESPN credentials.\n\n"
            "Things to check:\n"
            "  1. Log into https://fantasy.espn.com in one of your browsers\n"
            "     (Chrome, Firefox, Edge, Brave, or Safari)\n"
            "  2. Fully close that browser, then run this script again\n"
            "     (some browsers lock their cookie file while running)\n"
            "  3. Make sure you're a member of the private league\n"
        )
        sys.exit(1)

    print(f"Found credentials in {browser_name}!\n")
    print(f"SWID: {swid}")
    print(f"espn_s2: {espn_s2}")
    print("\nCopy both values above and send them back as instructed.")


if __name__ == "__main__":
    main()
