import requests
from bs4 import BeautifulSoup
from time import sleep


class ParsRandomPoety:
    def __init__(self):
        self.url = 'http://russian-poetry.ru/Random.php'
        self.r = requests.get(self.url)
        self.soup = BeautifulSoup(self.r.content, 'html.parser')

    def return_text(self):
        pre = self.soup.find('pre')
        pre = pre.text.split('\r')

        for elem in pre:
            if elem == '\n':
                pre.remove(elem)
        if ' ' not in pre[2].strip(',').strip('')[0]:
            return [pre[2].strip(',').strip('').replace('\n', '')[0:10], pre[2].strip(',').strip('').replace('\n', '') + ' ' + pre[3].strip(',').strip('').replace('\n', '')]
        else:
            return [pre[3].strip(',').strip('').replace('\n', '')[0:10], pre[3].strip(',').strip('').replace('\n', '') + ' ' + pre[4].strip(',').strip('').replace('\n', '')]


if __name__ == '__main__':
    prp = ParsRandomPoety()
    print(prp.return_text())
