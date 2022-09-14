import os


def main():
    print("Hello from Python!")
    print(f"This is the endpoint: {os.getenv('TIMESHEETS_ENDPOINT')}")


if __name__ == "__main__":
    main()
