class CacheKeys:

    @staticmethod
    def parser_lock(
        product_id: int | str
    ) -> str:

        return (
            f"parser_lock:"
            f"{product_id}"
        )

    @staticmethod
    def product(
        product_id: int | str
    ) -> str:

        return (
            f"product:"
            f"{product_id}"
        )

    @staticmethod
    def price_history(
        product_id: int | str
    ) -> str:

        return (
            f"price_history:"
            f"{product_id}"
        )

    @staticmethod
    def jwt_blacklist(
        jti: str
    ) -> str:

        return (
            f"jwt_blacklist:"
            f"{jti}"
        )

    @staticmethod
    def rate_limit(
        ip: str
    ) -> str:

        return (
            f"rate_limit:"
            f"{ip}"
        )