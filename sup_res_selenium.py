import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Настраиваем логирование
logging.basicConfig(filename='log.txt',
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class WebDriverManager:
    def __init__(self, debugger_address="127.0.0.1:9222"):
        self.driver = self._init_driver(debugger_address)

    def _init_driver(self, debugger_address):
        chrome_options = Options()
        chrome_options.debugger_address = debugger_address
        return webdriver.Chrome(options=chrome_options)

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        self.driver.quit()


class WebPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def find_window_by_url(self):
        all_windows = self.driver.window_handles
        for window in all_windows:
            self.driver.switch_to.window(window)
            if self.url in self.driver.current_url:
                return window
        return None

    def load_page(self):
        if not self.find_window_by_url():
            self.driver.get(self.url)
            time.sleep(0.1)


class FormFiller:
    def __init__(self, driver):
        self.driver = driver

    def fill_field(self, field_id, text, clear_first=True):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, field_id))
        )
        if clear_first:
            field.clear()
        field.send_keys(text)
        logging.info(f'Введен текст "{text}" в поле {field_id}')
        time.sleep(0.1)

    def select_option(self, field_id, options_down=4):
        field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, field_id))
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", field)
        field.click()

        for _ in range(options_down + 1):
            field.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.1)
        field.send_keys(Keys.RETURN)
        logging.info(f'Выбран {options_down + 1}-й элемент в {field_id}')
        time.sleep(1)

    def click_checkbox(self, css_selector, index):
        checkboxes = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        if len(checkboxes) <= index:
            raise Exception(f'{index + 1}-й элемент {css_selector} не найден')
        checkboxes[index].click()
        logging.info(f'Клик по {index + 1}-му checkbox')
        time.sleep(1)

    def click_outside(self):
        self.driver.find_element(By.TAG_NAME, 'body').click()
        logging.info('Клик вне области выбора')


class PostCreator:
    def __init__(self, driver, direction, title, currency_pair):
        self.driver = driver
        self.direction = direction
        self.title = title
        self.currency_pair = currency_pair

    def create_post(self):
        try:
            self._fill_title()
            time.sleep(0.3)
            self._fill_channel()
            time.sleep(0.3)

            self._fill_education_post()
            time.sleep(0.3)

            FormFiller(self.driver).click_outside()
            time.sleep(0.3)

            self._select_support()
            FormFiller(self.driver).click_outside()
            self._scroll_to_end()  # Scroll before selecting timeframe
            time.sleep(0.3)
            self._select_timeframe()
            self._scroll_to_end()  # Scroll after selecting timeframe
            self._check_trading_condition()
            self._scroll_to_end()  # Scroll after checking trading condition
            self._set_direction()
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            raise

    def _fill_title(self):
        FormFiller(self.driver).fill_field("title", self.title)

    def _fill_channel(self):
        FormFiller(self.driver).fill_field("channel", f'{self.currency_pair} support')
        channel_field = self.driver.find_element(By.ID, "channel")
        channel_field.send_keys(Keys.RETURN)

    def _fill_education_post(self):
        FormFiller(self.driver).fill_field("educationPost", 'breakout' if 'broke' in self.title else 'support')
        education_post_field = self.driver.find_element(By.ID, "educationPost")
        education_post_field.send_keys(Keys.RETURN)

    def _select_support(self):
        ant_select_inputs = self.driver.find_elements(By.CSS_SELECTOR, '.ant-select-selection-search input')
        logging.info(f'Найдено элементов ant-select-selection-search input: {len(ant_select_inputs)}')

        if len(ant_select_inputs) < 4:
            raise Exception('Третий элемент ant-select-selector не найден')

        ant_select_inputs[3].send_keys('support')
        ant_select_inputs[3].send_keys(Keys.RETURN)
        logging.info('Введен текст "support" и нажата клавиша Enter в третий ant-select-selector')

    def _scroll_to_end(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.info('Скролл до конца страницы')

    def _select_timeframe(self):
        FormFiller(self.driver).select_option("dealsAttribution_timeframe", options_down=3)

    def _check_trading_condition(self):
        FormFiller(self.driver).click_checkbox('.ant-checkbox-input', 1)

    def _set_direction(self):
        FormFiller(self.driver).fill_field("tradingCondition_direction", self.direction)
        direction_field = self.driver.find_element(By.ID, "tradingCondition_direction")
        if self.direction == "sell":
            direction_field.send_keys(Keys.ARROW_DOWN)
        direction_field.send_keys(Keys.RETURN)


def perform_action(direction, title, currency_pair):
    web_driver_manager = WebDriverManager()
    driver = web_driver_manager.get_driver()

    try:
        web_page = WebPage(driver, "https://cp.octafeed.com/panel/overview-posts/create")
        target_window = web_page.find_window_by_url()
        if target_window:
            logging.info(f"Используем найденную вкладку с URL: {driver.current_url}")
            driver.switch_to.window(target_window)
        else:
            logging.info("Не удалось найти вкладку с нужным URL, загружаем новую страницу")
            web_page.load_page()

        post_creator = PostCreator(driver, direction, title, currency_pair)
        post_creator.create_post()
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        web_driver_manager.quit_driver()
