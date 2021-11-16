# Local imports
from .solve_captcha import solve_normal_captcha

# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent

# Other imports
import os
import random
from time import sleep


# noinspection PyBroadException
class Yandex:
    def __init__(self, captcha_token, proxy, *data):
        self.captcha_token = captcha_token
        self.step = 'Прогрузка страницы. '
        self.data = [*data]
        self.filename = ''
        self.proxy = proxy
        self.PROXY = proxy.split(':')
        self.mail_url = 'https://mail.yandex.ua/'
        self.yandex_url = 'https://passport.yandex.ru/registration/mail?'

        # Options.
        self.useragent = UserAgent()
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("network.proxy.type", 1)
        self.profile.set_preference("network.proxy.http", str(self.PROXY[0]))
        self.profile.set_preference("network.proxy.http_port", int(self.PROXY[1]))
        # self.profile.set_preference("general.useragent.override", self.useragent.firefox)
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
        # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 5)
        self.longer = WebDriverWait(self.driver, 30)
        try:
            self.driver.get(self.yandex_url)
        except Exception as ex:
            self.driver.quit()
        sleep(2)
        self.driver.refresh()

    def pars_captcha(self):
        self.step = 'Парсинг капчи'
        try:
            sleep(2)
            # Пробуем нажать на 'разрешить куки' еще раз, если не сработало в первый.
            # В противном случае, просто пропускаем. Иногда эта кнопка не вылазит. Очередной баг yandex.ru.
            self.step = 'Подготовка к вводу данных в поле с капчей. '
            accept_btn = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/button')))
            accept_btn.click()
        except Exception as ex:
            pass
        self.step = 'Подготовка к вводу данных в поле с капчей. '
        sleep(2)
        captcha = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'captcha__image')))
        self.step = 'Сохранение .png капчи. '
        self.filename = self.filename.join(str(random.randint(0, 10)) for i in range(0, 10))
        captcha.screenshot(self.filename + '.png')

    def fill_the_field_test(self):
        self.step = 'Первый этап: заполнение формы. '
        # Toggle is a button 'I don't have a phone number'.
        try:
            # Пробуем нажать на кнопку принятия куки, если таковая появляется сразу.
            sleep(2)
            accept_btn = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/button')))
            accept_btn.click()
        except Exception as ex:
            pass
        self.step = 'Нажатие на кнопку "У меня нет телефона".'
        try:
            # Нажимаем на кнопку 'у меня нет телефона' и продолжаем работу.
            toggle = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/main/div/div/div/form/div[3]/div/div[2]/div/div[1]/span')))
            toggle.click()
        except Exception as ex:
            pass

        # Data to register.
        self.step = 'Нахождение всех полей для ввода данных. '
        text_inputs = self.wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'registration__label')))
        for i in range(6):
            # Вводим данные во все доступные поля.
            text_inputs[i].click()
            # ActionChains нам нужен, поскольку все поля прикрыты 'registration__label.
            # Этот "слой" не дает нам выполнять действия через обычный driver.click(), send_keys().
            # Так что, мы как бы 'Вручную вводим данные.
            actions = ActionChains(self.driver)
            actions.send_keys(self.data[i])
            actions.perform()
            actions.reset_actions()
        # Заполняем ответ на контрольный вопрос. Почему-то это поле не хочет заполняться вместе со всеми.
        # Посему, делаем так костыльно.
        self.step = 'Ввод ответа на контрольный вопрос. '
        self.answer = self.wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'registration__label')))
        self.answer[6].click()
        actions = ActionChains(self.driver)
        actions.send_keys(self.data[5])
        actions.perform()
        actions.reset_actions()

        # Выбор контрольного вопроса из списка. Выбираем один и тот же. Роли не играет.
        self.step = 'Выбор контрольного вопроса. '
        select_a_question = Select(self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'Select2-Control'))))
        select_a_question.select_by_visible_text('Марка вашей первой машины')

    def solve_captcha(self):
        # Решаем капчу.
        self.step = 'Решение капчи. '
        try:
            captcha_answer = solve_normal_captcha(self.filename + '.png', self.captcha_token)
        except Exception as ex:
            os.system(f'rm {self.filename}.png')
            print(ex)
            self.step = f'Решение капчи: {ex}'
        self.answer[7].click()
        action = ActionChains(self.driver)
        action.send_keys(captcha_answer)
        action.perform()
        sleep(1)
        self.step = 'Ввод капчи завершен. Нажимаем на кнопку. '

        submit = self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/span/button')
        submit.click()
        try:
            # Нажатие на кнопку, если всплывает вопрос 'Согласны ли вы с правилами конфеденциальности?'.
            submit_second = self.driver.find_element_by_xpath('/html/body/div/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button')
            submit_second.click()
        except Exception as ex:
            pass

        try:
            uncorrect_captcha = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/main/div/div/div/form/div[3]/div/div[2]/div[1]/div/div/div')))
            self.step = f'Введение и подтверждение капчи; ошибка: {uncorrect_captcha.text}'
        except Exception as ex:
            pass

        try:
            avatar_add = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div[2]/main/div/div/div/div[3]/span/a')))
            avatar_add.click()
        except Exception as ex:
            pass
        os.system(f'rm {self.filename}.png')

    def send_mail(self, receiver, msg):
        avatar = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[1]/header/div[2]/div[2]/div/div/a[1]/div/img')))
        avatar.click()
        sleep(2)

        self.step = 'Переход на почту. '
        mail_icon = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[1]/header/div[2]/div[2]/div/div/div/ul/ul/li[1]/a')))
        mail_icon.click()
        sleep(2)
        self.driver.refresh()

        try:
            close_popup = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[12]/div[2]/table/tbody/tr/td/div[1]')))
            close_popup.click()
        except Exception as ex:
            pass

        self.step = 'Подготовка к написанию письма.'
        write_a_msg = self.longer.until(ec.presence_of_element_located((By.CLASS_NAME, 'mail-ComposeButton-Text')))
        write_a_msg.click()

        try:
            close_popup = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[12]/div[2]/table/tbody/tr/td/div[1]')))
            close_popup.click()
        except Exception as ex:
            pass

        self.step = 'Ввод адреса отправителя. '
        rec_input = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[10]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[1]/div[1]/div/div/div/div/div')))
        rec_input.click()
        rec_input.send_keys(receiver)

        self.step = 'Ввод темы для отправки.'
        to_msg = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[10]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[1]/div[1]/div[3]/div/div/input')
        to_msg.click()
        to_msg.send_keys(f'Приветствие. ')

        self.step = 'Ввод сообщения для отправки'
        msg_field = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[10]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div[1]/div/div/div')
        msg_field.click()
        print(msg)
        msg_field.send_keys(msg)

        doit = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[10]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div[1]/button')
        doit.click()
        sleep(2)
        self.step = 'Успех!'

        try:
            statusline = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, 'b-statusline')))
            self.step = 'Сообщение ошибки при отправке сообщения: ' + statusline.text
        except Exception as ex:
            pass
        sleep(1)
        try:
            status_lin = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[10]/div/div/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div/div/div[1]/span')
            if status_lin.text == 'Письмо не отправлено':
                self.step = f'Сообщение отправлено, но с ошибкой: Письмо не отправлено, потому что текст письма похож на спам'
        except Exception as ex:
            pass

    def driver_close(self):
        self.driver.quit()

    def return_error(self):
        # Возвращаем ошибку.
        if self.step == 'Успех!':
            return 'Успех!'
        else:
            return f'Exception at the step: {self.step}'


if __name__ == '__main__':
    pass
