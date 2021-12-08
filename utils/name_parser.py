import random
import requests
from bs4 import BeautifulSoup
from transliterate import translit


class DataGen:
    def __init__(self, len_of_password, config_dir="config_txt"):
        self.config_dir = config_dir
        self.len_of_password = len_of_password
        # Letters to generate username with company's symblols.
        self.companies_letters = ['inc', 'pic', 'ltd', 'sa', 'sari', 'ag', 'gmbh', 'nv', 'bv', 'spa', 'srl', 'as']
        # Letters to generate passwords
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']
        # Numbers for a password.
        self.numbers = [x for x in range(0, 10)]

        # Urls for parsing boys and girls names.
        self.urls = ['https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%B8%D0%B5_%D0%B8%D0%BC%D0%B5%D0%BD%D0%B0',
                     'https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B5_%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B5_%D0%B8%D0%BC%D0%B5%D0%BD%D0%B0']
        self.lastname_url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BE%D0%B1%D1%89%D0%B5%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D1%85_%D1%84%D0%B0%D0%BC%D0%B8%D0%BB%D0%B8%D0%B9'

    def pars_data(self):
        # Pars first names.
        genders = ['boys', 'girls']
        for i in range(len(self.urls)):
            r = requests.get(self.urls[i])
            soup = BeautifulSoup(r.content, 'html.parser')

            category_group = soup.find_all('div', {'class': 'mw-category-group'})
            for category in category_group:
                ul_container = category.find_all('ul')
                for ul in ul_container:
                    name = ul.text.replace(' (имя)', '').replace(' (значения)', '').replace(' (женское имя)', '')

                    with open(self.config_dir+f'/{genders[i]}.txt', 'a+') as write_names:
                        write_names.write(name + '\n')
            r.close()
            soup.clear()

        # Pars last names.
        r = requests.get(self.lastname_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        columns = soup.find('div', {'class': 'columns'})
        ol = columns.find('ol')
        li_container = ol.find_all('li')
        for li in li_container:
            span = li.find('span')
            with open(self.config_dir+'/last_names.txt', 'a') as output:
                output.write(span.text + '\n')

    def data_for_register(self):
        # Read names.
        gender = random.choice(['boys', 'girls'])
        with open(self.config_dir+f'/{gender}.txt', 'r+', encoding='utf8') as read_names:
            name = read_names.read().strip().split('\n')

        # Read last names
        with open(self.config_dir+'/last_names.txt', 'r+', encoding='utf8') as last_names:
            surname = last_names.read().strip().split('\n')

        first_name = random.choice(name)
        last_name = random.choice(surname)
        username = f'{translit(first_name.lower(), reversed=True)}{translit(last_name.lower(), reversed=True)}{random.choice(self.companies_letters)}'
        password = ''.join(random.choice(self.letters) for self.i in range(self.len_of_password)) + \
                   random.choice(self.letters).upper() + str(random.choice(self.numbers))
        return [username.replace("'", ""), password, first_name, last_name]


if __name__ == '__main__':
    dg = DataGen(10)
    dg.pars_data()
