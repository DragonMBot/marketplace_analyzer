from app.parsers.ozon_parser import (
    OzonParser
)


class ParserFactory:

    @staticmethod
    def get_parser(
        marketplace: str
    ):

        if marketplace == "ozon":
            return OzonParser()

        raise ValueError(
            f"Unknown marketplace: {marketplace}"
        )