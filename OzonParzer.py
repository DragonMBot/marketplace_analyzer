import logging
from random import randint, random
from time import sleep
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ozon_parser.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OzonParser:
    def __init__(self, id_item):
        self.id_item = id_item
        self.price_dynamic_ozon = []
        self.price_dynamic_defolt = []
        logger.info(f"Инициализация парсера для товара id: {id_item}")

    def parse(self):
        logger.debug("Запуск метода parse()")
        try:
            with sync_playwright() as parser:
                logger.debug("Playwright запущен")
                browser = parser.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--window-size=1920,1080',
                    ]
                )
                logger.debug("Браузер Chromium запущен")
                self.context = browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                self.page = self.context.new_page()
                logger.debug("Создана новая страница")

                try:
                    logger.info("Переход на https://www.ozon.ru/")
                    self.page.goto("https://www.ozon.ru/", timeout=30000)
                    logger.debug("Главная страница загружена")
                except PlaywrightTimeoutError:
                    logger.error("Таймаут при загрузке главной страницы Ozon")
                    raise
                except PlaywrightError as e:
                    logger.error(f"Ошибка Playwright при переходе на главную страницу: {e}")
                    raise

                try:
                    search_input = self.page.get_by_placeholder("Искать на Ozon")
                    if not search_input:
                        logger.error("Не найдено поле ввода с плейсхолдером 'Искать на Ozon'")
                        raise Exception("Поле поиска не обнаружено")
                    delay = randint(1, 2) + round(random(), 2)
                    logger.debug(f"Ввод текста '{self.id_item}' с задержкой {delay} сек")
                    search_input.type(text=self.id_item, delay=delay)
                except PlaywrightError as e:
                    logger.error(f"Ошибка при вводе текста в поисковую строку: {e}")
                    raise

                try:
                    submit_button = self.page.query_selector("button[type='submit']")
                    if not submit_button:
                        logger.error("Не найдена кнопка отправки формы поиска")
                        raise Exception("Кнопка поиска отсутствует")
                    logger.debug("Клик по кнопке поиска")
                    submit_button.click()
                except PlaywrightError as e:
                    logger.error(f"Ошибка при клике по кнопке поиска: {e}")
                    raise

                logger.info("Ожидание загрузки страницы результатов (5 сек)")
                sleep(5)

                try:
                    title_selector = "span[class='tsHeadline600Large']"
                    title_element = self.page.query_selector(title_selector)
                    if title_element:
                        title_text = title_element.text_content()
                        logger.info(f"Цена товара озон карта: {title_text}")
                        print(title_text)
                    else:
                        logger.warning(f"Элемент не найден по селектору: {title_selector}")
                        print("Цена товара озон карта не найдена")

                    price_selector = "span[class='pdp_jb tsHeadline500Medium']"
                    price_element = self.page.query_selector(price_selector)
                    if price_element:
                        price_text = price_element.text_content()
                        logger.info(f"Цена товара обычная: {price_text}")
                        print(price_text)
                    else:
                        logger.warning(f"Элемент цены не найден по селектору: {price_selector}")
                        print("Цена обычная не найдена")

                except PlaywrightError as e:
                    logger.error(f"Ошибка при извлечении данных со страницы: {e}")

                sleep(5)
                logger.debug("Парсинг завершён")

                browser.close()
                logger.debug("Браузер закрыт")

        except Exception as e:
            logger.critical(f"Необработанное исключение в методе parse(): {e}", exc_info=True)
            raise

if __name__ == "__main__":
    logger.info("=== Запуск парсера Ozon ===")
    try:
        OzonParser("3354536018").parse()
        logger.info("Парсинг успешно завершён")
    except Exception as e:
        logger.error(f"Программа завершилась с ошибкой: {e}")