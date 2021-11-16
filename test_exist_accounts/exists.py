from time import sleep

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys


# noinspection PyBroadException
class CheckYandex:
    def __init__(self, proxy: str):
        self.step = ''
        self.url = 'https://mail.yandex.ru/'

        self.PROXY = proxy.split(':')
        # Options.
        self.useragent = UserAgent()
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("network.proxy.type", 1)
        self.profile.set_preference("network.proxy.http", str(self.PROXY[0]))
        self.profile.set_preference("network.proxy.http_port", int(self.PROXY[1]))
        self.profile.set_preference('dom.webdriver.enabled', False)
        self.profile.set_preference('useAutomationExtension', False)
        self.profile.set_preference("intl.accept_languages", "en-en")
        self.profile.set_preference("media.volume_scale", "0.0")
        self.profile.update_preferences()

        self.firecap = webdriver.DesiredCapabilities.FIREFOX
        self.firecap['marionette'] = True
        self.firecap['proxy'] = {
            'proxyType': 'MANUAL',
            'httpProxy': proxy,
            'sslProxy': proxy
        }
        self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                        proxy=self.firecap,
                                        )
        self.wait = WebDriverWait(self.driver, 5)
        self.longer = WebDriverWait(self.driver, 30)
        self.driver.get(self.url)

    def login(self, mail, passwd):
        try:
            login_btn = self.wait.until(ec.presence_of_element_located((By.LINK_TEXT, 'Войти')))
            login_btn.click()
        except Exception as ex:
            pass
        # Вводим данные для входа в аккаунт.
        mail_field = self.wait.until(ec.presence_of_element_located((By.ID, 'passp-field-login')))
        mail_field.click()
        mail_field.send_keys(mail + Keys.ENTER)
        try:
            err_msg = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="field:input-passwd:hint"]')))
            self.step = err_msg
            print(self.step)
            self.driver.close()
        except Exception as ex:
            print(ex)

        passwd_field = self.wait.until(ec.presence_of_element_located((By.ID, 'passp-field-passwd')))
        passwd_field.click()
        passwd_field.send_keys(passwd + Keys.ENTER)

        try:
            err_msg = self.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="field:input-passwd:hint"]')))
            self.step = err_msg
            print(self.step)
            self.driver.close()
        except Exception as ex:
            print(ex)

    def handle_an_error(self):
        # Пытаемся распарсить всплывающее окно об ошибке.
        # Если не получется - проверяем наличие сообщения на странице о взломе(например что-то вроде 'Изменение пароля')
        try:
            error_msg = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'error-msg')))
            self.step = f'Error: {error_msg.text}'
            self.driver.close()
        except Exception:
            try:
                head = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'head')))
                self.step = f'Error: {head.text}'
            except Exception:
                pass

    def check_messages(self):
        # Проверяем последнее сообщение.
        try:
            last_messages = self.wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'b-messages__message b-messages__message_unread b-messages__message_last')))
            self.step = f'Успех: последнее сообщение: {last_messages[0]}'
        except Exception as ex:
            self.step = 'Мы успешно зашли на аккаунт, но найти последние сообщения не вышло. '

    def return_an_error(self):
        return self.step

    def driver_close(self):
        self.driver.close()


class CheckRambler:
    def __init__(self, proxy):
        self.step = ''
        self.url = 'https://mail.rambler.ru/'

        self.PROXY = proxy.split(':')
        # Options.
        self.useragent = UserAgent()
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("network.proxy.type", 1)
        self.profile.set_preference("network.proxy.http", str(self.PROXY[0]))
        self.profile.set_preference("network.proxy.http_port", int(self.PROXY[1]))
        self.profile.set_preference("general.useragent.override", self.useragent.firefox)
        self.profile.set_preference('dom.webdriver.enabled', False)
        self.profile.set_preference('useAutomationExtension', False)
        self.profile.set_preference("intl.accept_languages", "en-en")
        self.profile.set_preference("media.volume_scale", "0.0")
        self.profile.update_preferences()

        self.firecap = webdriver.DesiredCapabilities.FIREFOX
        self.firecap['marionette'] = True
        self.firecap['proxy'] = {
            'proxyType': 'MANUAL',
            'httpProxy': proxy,
            'sslProxy': proxy
        }
        self.driver = webdriver.Firefox(firefox_profile=self.profile,
                                        proxy=self.firecap,
                                        )
        self.wait = WebDriverWait(self.driver, 5)
        self.longer = WebDriverWait(self.driver, 30)
        self.driver.get(self.url)

    def login(self, mail, passwd):
        login = self.wait.until(ec.presence_of_element_located((By.ID, 'login')))
        login.click()
        login.send_keys(mail)

        password = self.wait.until(ec.presence_of_element_located((By.ID, 'password')))
        password.click()
        password.send_keys(passwd)

        submit = self.driver.find_element_by_xpath('/html/body/div[1]/div/div/div/article/form/button/span')
        submit.click()

    def handle_login_error(self):
        try:
            error_msg = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'rui-FieldStatus-message')))
            self.step = f'Error message: {error_msg.text}'
        except Exception as ex:
            pass

    def check_messages(self):
        sleep(3)
        self.driver.get(self.url)
        list_item = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'ListItem-root-1i ListItem-unseen-kd')))
        self.step = f'Успех! Ваше последнее сообщение: {list_item}'

    def return_an_error(self):
        return self.step

    def driver_close(self):
        self.driver.close()


if __name__ == '__main__':
    cy = CheckYandex('')

