from time import sleep
from random import randint
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Rambler:
    def __init__(self, proxy):
        self.success_status = ''
        self.step = 'Прогрузка страницы. '
        self.PROXY = proxy.split(':')
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
        self.rambler_url = 'https://id.rambler.ru/login-20/mail-registration?rname=head&back=https%3A%2F%2Fwww.rambler.ru%2F&param=popup&iframeOrigin=https%3A%2F%2Fwww.rambler.ru'
        self.driver = webdriver.Firefox(proxy=self.firecap, firefox_profile=self.profile)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 5)
        self.longer = WebDriverWait(self.driver, 30)
        self.driver.get(self.rambler_url)
        print(self.driver.execute_script('return navigator.userAgent;'))

    def pars_captcha_image(self):
        self.step = 'Парсинг url нашей captcha. '
        captcha = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/article/form/section[2]/div/div/div[1]/img')))
        return captcha.get_attribute('src')

    def fill_the_fields(self, mail, password, answer_on_the_question):
        self.step = 'Ввод логина. '
        login = self.wait.until(ec.presence_of_element_located((By.ID, 'login')))
        login.click()
        login.send_keys(mail)

        self.step = 'Ввода пароля. '
        first_passwd = self.wait.until(ec.presence_of_element_located((By.ID, 'newPassword')))
        first_passwd.click()
        first_passwd.send_keys(password)

        confirm_passwd = self.wait.until(ec.presence_of_element_located((By.ID, 'confirmPassword')))
        confirm_passwd.click()
        confirm_passwd.send_keys(password)

        question = self.driver.find_element_by_id('question')
        question.click()

        sleep(2)
        self.step = 'Выбор случайного контрольного вопроса. '
        # rul_menu_items = self.driver.find_elements_by_class_name('rui-Select-menuItem')
        rul_menu_items = self.wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'rui-Select-menuItem')))
        ran_question = randint(0, len(rul_menu_items)-2)
        rul_menu_items[ran_question].click()
        sleep(2)

        self.step = 'Ввод ответа на контрольный вопрос. '
        answer = self.driver.find_element_by_id('answer')
        answer.click()
        answer.send_keys(answer_on_the_question)
        sleep(1)

    def answer_to_the_captcha(self, captcha_answer):
        self.step = 'Вводим капчу. '
        submit_captcha = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/article/form/section[2]/div/div/div[2]/div/div[1]/input')
        submit_captcha.click()
        submit_captcha.send_keys(captcha_answer)

        self.step = 'Подтверждение введенных данных. '
        submit = self.driver.find_element_by_class_name('rui-Button-content')
        submit.click()
        sleep(10)

    def handle_an_error(self):
        try:
            # captcha_error = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/article/form/section[2]/div/div/div[2]/div/div[2]')))
            captcha_error = self.driver.find_elements_by_class_name('rui-FieldStatus-message')
            self.step = captcha_error[len(captcha_error)-1].text
        except Exception as ex:
            pass

    def fill_the_personal_information(self, name, surname, region):
        self.step = 'Начинаем заполнение персональной информации. '
        firstname = self.wait.until(ec.presence_of_element_located((By.ID, 'firstname')))
        firstname.click()
        firstname.send_keys(name)

        self.step = 'Вводим фамилию. '
        lastname = self.driver.find_element_by_id('lastname')
        lastname.click()
        lastname.send_keys(surname)

        self.step = 'Выбираем дату рождения. '
        select_birthday = self.wait.until(ec.presence_of_element_located((By.ID, 'birthday')))
        select_birthday.click()
        sleep(2)
        self.step = 'Выбираем дату рождения из выпавшего списка.'
        rul_menu_item = self.driver.find_elements_by_class_name('rui-Select-menuItem')
        rul_menu = randint(0, 29)
        rul_menu_item[rul_menu].click()

        self.step = 'Выбираем месяц рождения. '
        select_month = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/article/form/section[4]/div/div/div[1]/div[2]/div/div/div/input')
        select_month.click()
        rul_menu_month = self.driver.find_elements_by_class_name('rui-Select-menuItem')
        rul_month = randint(0, 11)
        rul_menu_month[rul_month].click()

        self.step = 'Выбираем год рождения. '
        select_year = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/article/form/section[4]/div/div/div[1]/div[3]/div/div/div/input')
        select_year.click()
        rul_menu_year = self.driver.find_elements_by_class_name('rui-Select-menuItem')
        rul_year = randint(26, 46)
        rul_menu_year[rul_year].click()

        self.step = 'Выбираем пол. '
        select_gender = self.driver.find_element_by_id('gender')
        select_gender.click()
        gender_rul = self.driver.find_elements_by_class_name('rui-Select-menuItem')
        gen_rul = randint(0, 1)
        gender_rul[gen_rul].click()

        self.step = 'Вводим регион(geoid). '
        geoid = self.driver.find_element_by_id('geoid')
        geoid.click()
        geoid.send_keys(region + Keys.ENTER)
        geoid.send_keys(Keys.ENTER)
        sleep(1)
        self.success_status = 'Аккаунт зарегистрирован!'

    def send_a_message(self, receiver, msg):
        self.driver.get('https://mail.rambler.ru/')
        # self.step = 'Нажатие на иконку почту на главной rambler.ru.'
        # mail_icon = self.wait.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/main/div[2]/div/div/div/div/div[4]/div/a')))
        # mail_icon.click()
        self.step = 'Переход во вкладку "Отправить". '
        send_mail = self.longer.until(ec.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/div[1]/div[1]/button/span')))
        send_mail.click()

        receivers = self.driver.find_element_by_id('receivers')
        receivers.click()
        receivers.send_keys(receiver)

        subject = self.driver.find_element_by_id('subject')
        subject.click()
        subject.send_keys('Приветствую!')

        tinymce = self.driver.find_element_by_xpath('/html/body/div')
        tinymce.click()
        action = ActionChains(self.driver)
        action.send_keys(msg).perform()
        self.step = 'Успех!'

    def driver_close(self):
        self.driver.quit()

    def return_error(self):
        if self.step == 'Успех':
            return self.step
        else:
            if self.success_status == 'Аккаунт зарегистрирован!':
                return f'Аккаунт зарегистрирован успешно, но с ошибкой при отправке сообщения: {self.step}'
            else:
                return f'Exception at the step: {self.step}'


if __name__ == '__main__':
    r = Rambler('')
