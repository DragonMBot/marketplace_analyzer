import json
import webbrowser
import logging
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("price_chart.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def parse_data(data_list):
    dates = []
    prices = []

    logger.debug("Начало парсинга данных")
    for idx, item in enumerate(data_list):
        if not isinstance(item, dict):
            err_msg = f"Элемент {idx} не является словарём: {type(item)}"
            logger.error(err_msg)
            raise ValueError(err_msg)

        for date_str, price in item.items():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                dates.append(date_obj)
                prices.append(float(price))
                logger.debug(f"Успешно распознана дата: {date_str} -> {date_obj}, цена: {price}")
            except ValueError as e:
                logger.warning(f"Не удалось распознать дату '{date_str}': {e}. Используется как строка.")
                dates.append(date_str)
                prices.append(float(price))
            except Exception as e:
                logger.error(f"Непредвиденная ошибка при обработке пары ({date_str}: {price}): {e}")
                raise

    if dates and all(isinstance(d, datetime) for d in dates):
        logger.debug("Сортировка данных по дате (datetime)")
        sorted_pairs = sorted(zip(dates, prices), key=lambda x: x[0])
        dates, prices = zip(*sorted_pairs) if sorted_pairs else ([], [])
        dates = list(dates)
        prices = list(prices)
        logger.debug("Сортировка завершена")
    else:
        logger.info("Некоторые даты не являются datetime, сортировка не выполнена")

    logger.info(f"Парсинг завершён. Получено {len(dates)} точек данных.")
    return dates, prices


def create_price_chart(dates, prices, title="График цен по датам"):
    logger.debug("Создание графика")
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines+markers',
        name='Цена',
        line=dict(color='royalblue', width=2),
        marker=dict(size=6, color='red')
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Дата",
        yaxis_title="Цена",
        hovermode="x unified",
        template="plotly_white"
    )

    if dates and isinstance(dates[0], datetime):
        fig.update_xaxes(
            tickformat="%Y-%m-%d",
            tickangle=45,
            title_text="Дата"
        )
        logger.debug("Ось X настроена для datetime")
    else:
        logger.debug("Ось X настроена для строковых дат")

    logger.info("График успешно создан")
    return fig


def main(data_list=None, input_file=None, output_html="price_chart.html"):
    logger.info("=== Запуск main() ===")

    if input_file:
        try:
            logger.info(f"Загрузка данных из файла: {input_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            logger.debug(f"Файл {input_file} успешно загружен")
        except FileNotFoundError:
            logger.error(f"Файл не найден: {input_file}")
            print(f"Ошибка: файл {input_file} не существует.")
            return
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка разбора JSON в файле {input_file}: {e}")
            print(f"Ошибка: файл {input_file} содержит некорректный JSON.")
            return
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при чтении файла {input_file}: {e}", exc_info=True)
            print(f"Ошибка чтения файла: {e}")
            return

    if not data_list:
        logger.warning("Нет данных для построения графика (data_list пуст)")
        print("Нет данных для построения графика.")
        return

    try:
        dates, prices = parse_data(data_list)
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}", exc_info=True)
        print(f"Ошибка обработки данных: {e}")
        return

    if not dates:
        logger.warning("Не найдено ни одной корректной пары дата-цена")
        print("Не найдено ни одной корректной пары дата-цена.")
        return

    try:
        fig = create_price_chart(dates, prices)
    except Exception as e:
        logger.error(f"Ошибка при создании графика: {e}", exc_info=True)
        print(f"Ошибка при создании графика: {e}")
        return

    try:
        fig.write_html(output_html)
        logger.info(f"График сохранён в {output_html}")
        print(f"График сохранён в {output_html}")
    except Exception as e:
        logger.error(f"Ошибка при записи HTML-файла {output_html}: {e}", exc_info=True)
        print(f"Ошибка сохранения графика: {e}")
        return

    try:
        file_url = f"file://{Path(output_html).absolute()}"
        logger.debug(f"Открытие {file_url} в браузере")
        webbrowser.open(file_url)
        logger.info("График открыт в браузере")
    except Exception as e:
        logger.error(f"Не удалось открыть браузер: {e}", exc_info=True)
        print(f"Не удалось открыть браузер: {e}")

    logger.info("=== main() завершён ===")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    sample_data = [
        {"2024-01-01": 150.5},
        {"2024-01-02": 160.0},
        {"2024-01-03": 155.2},
        {"2024-01-04": 170.8},
        {"2024-01-05": 165.3}
    ]

    try:
        main(data_list=sample_data)
    except Exception as e:
        logger.critical(f"Необработанное исключение в программе: {e}", exc_info=True)
        print(f"Критическая ошибка: {e}")