from time import sleep
# local files.
from gen import *
from utils.yandex import Yandex
from utils.rambler import Rambler

from utils.checking_proxy import checkout_proxy
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
        ip = [
            '146.59.18.78:5000',
            '146.59.18.78:5001',
            '146.59.18.78:5002',
            '146.59.18.78:5003',
            '146.59.18.78:5004',
            '146.59.18.78:5005',
            '146.59.18.78:5006'
        ]
        while True:
            with Pool(6) as pl:
                all_p = pl.map(checkout_proxy, ip)
            filtred_list = filter(None.__ne__, all_p)
            list_of_ip = list(filtred_list)
            if len(list_of_ip) > 0:
                break
            sleep(5)
        if len(list_of_ip) > 1:
            # fake_auth_rambler(random.choice(list_of_ip), 'mail@rambler.ru', 'passwd')
            # fake_auth_yandex(random.choice(list_of_ip), 'militsakulagininc@yandex.ru', 'zserovklkjS5')
            print(register_yandex_account(random.choice(list_of_ip), 'nikita07050565@gmail.com', '587090417529ff6968eb9f0cb806c0e9'))
            # print(register_rambler_account(random.choice(list_of_ip), 'nikita07050565@gmail.com', '587090417529ff6968eb9f0cb806c0e9'))
        if len(list_of_ip) == 1:
            # fake_auth_rambler(list_of_ip[0], 'mail@rambler.ru', 'passwd')
            # fake_auth_yandex(list_of_ip[0], 'militsakulagininc@yandex.ru', 'zserovklkjS5')
            print(register_yandex_account(list_of_ip[0], 'nikita07050565@gmail.com', '587090417529ff6968eb9f0cb806c0e9'))
            # print(register_rambler_account(list_of_ip[0], 'nikita07050565@gmail.com', '587090417529ff6968eb9f0cb806c0e9'))
        break
