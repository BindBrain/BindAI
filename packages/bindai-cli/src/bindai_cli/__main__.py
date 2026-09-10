from bindai_providers import bootstrap

from bindai_cli.app import app


def main():
    bootstrap()
    app()


if __name__ == "__main__":
    main()
