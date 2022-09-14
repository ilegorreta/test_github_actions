import os
import requests

TEST_URL = os.getenv("TEST_URL")
API_AUTH = os.getenv("ROSTER_AUTH")


def main():
    payload = {}
    headers = {"Authorization": API_AUTH}
    response = requests.request("GET", TEST_URL, headers=headers, data=payload)
    print(response.text)


if __name__ == "__main__":
    main()
