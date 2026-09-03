from bindai_cli.app import app
from bindai_providers import bootstrap


def main():
    bootstrap()
    app()


if __name__ == "__main__":
    main()