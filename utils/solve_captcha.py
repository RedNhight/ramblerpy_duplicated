from twocaptcha import TwoCaptcha


def solve_normal_captcha(captcha_image, twocaptcha_token):
    solver = TwoCaptcha(twocaptcha_token)
    result = solver.normal(file=captcha_image, lang='ru')
    return result['code']
