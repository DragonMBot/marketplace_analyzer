import time
from random import randint

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError
)

from app.core.logger import logger

from app.parsers.base import ProductPriceData

from app.monitoring.metrics import (
    parser_runs_total,
    parser_errors_total,
    parser_duration_seconds,
    active_parsers,
    playwright_browser_launch_total,
    playwright_browser_errors_total,
    playwright_page_load_seconds
)


class OzonParser:
    """
    Production Ozon parser using Playwright.
    """

    MARKETPLACE = "ozon"

    def parse(self, product_id: str) -> ProductPriceData:

        start_time = time.perf_counter()

        parser_runs_total.labels(
            marketplace=self.MARKETPLACE
        ).inc()

        active_parsers.inc()

        logger.info(
            f"[OZON PARSER] Start parsing: {product_id}"
        )

        browser = None

        try:

            with sync_playwright() as p:

                playwright_browser_launch_total.inc()

                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu"
                    ]
                )

                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 "
                        "(Windows NT 10.0; Win64; x64)"
                    )
                )

                page = context.new_page()

                page_start = time.perf_counter()

                try:

                    page.goto(
                        "https://www.ozon.ru/",
                        timeout=30000
                    )

                    playwright_page_load_seconds.labels(
                        marketplace=self.MARKETPLACE
                    ).observe(
                        time.perf_counter() - page_start
                    )

                except PlaywrightTimeoutError as exc:

                    playwright_browser_errors_total.inc()

                    parser_errors_total.labels(
                        marketplace=self.MARKETPLACE
                    ).inc()

                    logger.error(
                        f"Ozon load timeout: {exc}"
                    )

                    raise

                # ====================================================
                # SEARCH
                # ====================================================

                search_input = page.get_by_placeholder(
                    "Искать на Ozon"
                )

                search_input.type(
                    product_id,
                    delay=randint(50, 120)
                )

                page.click(
                    "button[type='submit']"
                )

                page.wait_for_timeout(5000)

                # ====================================================
                # TITLE
                # ====================================================

                title = None
                current_price = None

                title_element = page.query_selector(
                    "span[class*='tsHeadline']"
                )

                if title_element:
                    title = title_element.text_content()

                # ====================================================
                # PRICE (fallback selectors)
                # ====================================================

                price_selectors = [
                    "span[class*='pdp_jb']",
                    "span[data-widget='webPrice']",
                    "span[class*='price']"
                ]

                for selector in price_selectors:

                    price_element = page.query_selector(selector)

                    if price_element:

                        text = price_element.text_content()

                        if text:

                            text = (
                                text.replace("₽", "")
                                .replace(" ", "")
                                .strip()
                            )

                            try:
                                current_price = float(text)
                                break
                            except ValueError:
                                continue

                browser.close()

                duration = time.perf_counter() - start_time

                parser_duration_seconds.labels(
                    marketplace=self.MARKETPLACE
                ).observe(duration)

                logger.info(
                    f"[OZON PARSER] Done "
                    f"{product_id} "
                    f"in {duration:.2f}s"
                )

                return ProductPriceData(
                    external_id=product_id,
                    title=title,
                    current_price=current_price,
                    old_price=None,
                    marketplace=self.MARKETPLACE
                )

        except Exception as exc:

            parser_errors_total.labels(
                marketplace=self.MARKETPLACE
            ).inc()

            playwright_browser_errors_total.inc()

            logger.exception(
                f"[OZON PARSER ERROR] {product_id}: {exc}"
            )

            return ProductPriceData(
                external_id=product_id,
                title=None,
                current_price=None,
                old_price=None,
                marketplace=self.MARKETPLACE
            )

        finally:

            active_parsers.dec()

            if browser:
                try:
                    browser.close()
                except Exception:
                    pass