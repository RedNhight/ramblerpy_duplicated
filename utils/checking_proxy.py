from proxy_checker import ProxyChecker


def checkout_proxy(address):
    checker = ProxyChecker()
    result = checker.check_proxy(f'{address}')
    if result is not False:
        if result['timeout'] < 200:
            print(result)
            if 'http' in result['protocols'] or 'https' in result['protocols']:
                if result['country'] != '-':
                    return address
            else:
                print(f"{address} is a {result['protocols']} IP. Not HTTP. ")
        else:
            print(f"{address}: Timeout!")
    else:
        print(f"{address} isn't valid. ")


if __name__ == '__main__':
    pass
