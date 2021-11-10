from utils.name_parser import DataGen
from utils.pars_answers import ParsRandomPoety


def reg_form(config_dir="config_txt"):
    dg = DataGen(10, config_dir)
    form = dg.data_for_register()
    return form


def poety():
    prp = ParsRandomPoety()
    text = prp.return_text()[0][:10]
    while text.strip() == "":
        prp = ParsRandomPoety()
        text = prp.return_text()[:10]
    print(text)
    return text


if __name__ == '__main__':
    data = reg_form()

