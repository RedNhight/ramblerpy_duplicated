from random import choice
from unittest import TestCase
from local_config import *
from fosy_proxy_tools import *
from main import *


class Test(TestCase):
    def test_callback_yandex(self):
        fosy_proxy = FosyProxyTools(FOSY_KEY)
        receivers = [TEST_RECEIVER]
        accounts = []
        for i in range(0, 5):
            current_proxy = fosy_proxy.get_proxy("http")
            account = register_yandex_account(current_proxy, choice(receivers), TWOCAPTCHA_TOKEN)
            print(account['result'])
            print(account['mail'])
            print(account['password'])
            if account['result'] == "Успех!":
                receivers.append(account['mail'])
                accounts.append(account)
        if len(accounts) > 0:
            for account in accounts:
                current_proxy = fosy_proxy.get_proxy("http")
                result = fake_auth_yandex(current_proxy, account['mail'], account['password'])
                print(result)
                self.assertRegex(result, "^Успех:.*", "Result: "+result)


if __name__ == '__main__':
    t = Test()
    t.test_callback_yandex()
