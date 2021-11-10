from twocaptcha import TwoCaptcha


def solve_normal_captcha(captcha_image, twocaptcha_token):
    solver = TwoCaptcha(twocaptcha_token)
    result = solver.normal(file=captcha_image, lang='ru')
    return result['code']


if __name__ == '__main__':
    solve_normal_captcha('/home/penguin_nube/main_files/rambler_auth/utils/123.png')
