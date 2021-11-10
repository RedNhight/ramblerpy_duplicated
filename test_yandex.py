from unittest import TestCase
from .local_config import *
from .fosy_proxy_tools import *
from .main import register_yandex_account

from random import choice
from unittest import TestCase
from local_config import *
from fosy_proxy_tools import *
from main import *


class Test(TestCase):
    def test_callback_yandex(self):
        fosy_proxy = FosyProxyTools(FOSY_KEY)
        current_proxy = fosy_proxy.get_proxy("http")
        register_yandex_account(current_proxy, TEST_RECEIVER, TWOCAPTCHA_TOKEN)
        self.fail("Not finished")
        receivers = [TEST_RECEIVER]
        accounts = []
        for i in range(0,10):
            current_proxy = fosy_proxy.get_proxy("http")
            account = register_yandex_account(current_proxy, choice(receivers), TWOCAPTCHA_TOKEN)
            if (account.result == "Успех!"):
                receivers.append(account.login)
                accounts.append(account)

        for account in accounts:
            current_proxy = fosy_proxy.get_proxy("http")
            result = fake_auth_yandex(current_proxy, account.login, account.password)
            self.assertRegex(result, "^Успех:.*", "Result: "+result)

