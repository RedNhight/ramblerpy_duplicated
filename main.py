from time import sleep
# local files.
from gen import *
from utils.yandex import Yandex
from utils.rambler import Rambler

from utils.solve_captcha import solve_normal_captcha
from test_exist_accounts.exists import CheckYandex, CheckRambler

# Libraries.
import random
from multiprocessing import Pool


def fake_auth_yandex(proxy, mail, passwd):
    cy = CheckYandex(proxy)
    try:
        cy.login(mail, passwd)
        cy.handle_an_error()
        cy.check_messages()
        cy.driver_close()
    except Exception as ex:
        cy.driver_close()
    print(cy.return_an_error())
    return cy.return_an_error()


def fake_auth_rambler(proxy, mail, passwd):
    cr = CheckRambler(proxy)
    try:
        cr.login(mail, passwd)
        cr.handle_login_error()
        cr.check_messages()
    except Exception as ex:
        pass
    cr.driver_close()
    print(cr.return_an_error())
    return cr.return_an_error()


def register_yandex_account(proxy, receiver, twocaptcha_token):
    # Generate random data for register.
    prp = ParsRandomPoety()
    ptp = prp.return_text()
    rf = reg_form()
    print(rf[1])
    print(rf[0])
    y = Yandex(twocaptcha_token, proxy, rf[2], rf[3], rf[0], rf[1], rf[1], ptp[0])
    try:
        # Initialize Yandex class.
        y.fill_the_field_test()
        y.pars_captcha()

        y.solve_captcha()
        sleep(4)
        # y.send_mail(receiver=receiver, msg=f'Приветствую, {rf[2]} {rf[3]}. ::: {ptp[1]}')
    except Exception as ex:
        y.driver_close()
    error_step = y.return_error()
    y.driver_close()
    y.gl.stop()
    print(rf[1])
    print(rf[0])
    result = {
        'result': error_step,
        'mail': f'{rf[0]}@yandex.ru',
        'password': rf[1],
        'secret': ptp[0]
    }
    return result


def register_rambler_account(proxy, mail_to_receive, twocaptcha_token):
    r = Rambler(proxy)
    rf = reg_form()
    prp = ParsRandomPoety()
    txt = prp.return_text()
    try:
        regions = ['Черниговская область', 'Киевская область',
                   'Кировоградская область', 'Московская область',
                   'Амурская область', 'Архангельская область',
                   'Челябинская область', 'Иркутская область', 'Ивановская область']

        r.fill_the_fields(mail=rf[0],
                          password=rf[1],
                          answer_on_the_question=txt[0],
                          )
        try:
            captcha_image = r.pars_captcha_image()
            captcha_code = solve_normal_captcha(captcha_image, twocaptcha_token)
            r.answer_to_the_captcha(captcha_answer=captcha_code)
        except Exception as ex:
            print(ex)
            r.step = 'ERROR_ZERO_BALANCE'

        if r.step != 'ERROR_ZERO_BALANCE':
            r.handle_an_error()
            r.fill_the_personal_information(rf[2], rf[3], random.choice(regions))
            r.send_a_message(mail_to_receive, txt[1])
    except Exception as ex:
        pass
    r.driver_close()
    result = {
        'result': r.return_error(),
        'mail': f'{rf[0]}@rambler.ru',
        'password': rf[1],
        'secret': txt[0]

    }
    return result


if __name__ == '__main__':
    while True:
        with open('logins.txt', 'a') as log_txt:
            acc = register_yandex_account('', 'nikita07050565@gmail.com', '30a16da13415eb8c24eacb22428b9c0b')
            if acc['result'] == 'Успех!':
                log_txt.write(acc['mail'] + ':' + acc['password'] + ':' + acc['secret'] + '\n')
