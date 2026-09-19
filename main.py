from app.services.investigator import investigate_transaction


def main() -> None:
    result = investigate_transaction("TX9999")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
