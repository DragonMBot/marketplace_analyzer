from app.parsers.parser_factory import (
    ParserFactory
)


class ParserService:

    async def parse_product(
        self,
        marketplace: str,
        external_id: str
    ):

        parser = (
            ParserFactory.get_parser(
                marketplace
            )
        )

        return parser.parse(
            external_id
        )