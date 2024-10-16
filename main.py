import requests
import xml.etree.ElementTree
import json
from datetime import datetime
import os.path


class Liba: #Класс хранит соответствие портфель-файл с данными портфеля
    def __init__(self):
        if os.path.isfile('pfos.txt'): #при инициализации создает такой файл либо просто узнает, кто в нем есть
            with open('pfos.txt', 'r') as f:
                self.pfos = [x.rstrip('\n').split('|') for x in f.readlines()]
        else:
            with open('pfos.txt', 'w') as f:
                self.pfos = []

class Portfolio:
    def __init__(self, cash, fname, portfname):
        self.__fname = fname
        db = datetime.now().strftime('%d %b %H:%M')
        to_json = {'cash': cash, 'datebirth': db, 'pnl': 0}
        with open(fname + '.json', 'w') as f:
            json.dump(to_json, f)

        with open('pfos.txt', 'a') as f:
            f.write(portfname + '|' + fname + '\n')

    def free_cash(self):
        with open(self.__fname + '.json') as f:
            sl = f.read()
            dict_obj = json.loads(sl)
            return dict_obj['cash']

    def date_birth(self):
        with open(self.__fname + '.json') as f:
            sl = f.read()
            dict_obj = json.loads(sl)
            return dict_obj['datebirth']


class Stock:
    def cur_price(self):
        """Текущая цена по этому тикеру"""
        s = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/" + self.ticker + ".xml?iss.meta=off"
        r = requests.get(s)
        root = xml.etree.ElementTree.fromstring(r.content)
        for data in root.findall("data"):
            if data.get("id") == "marketdata":
                rows = data.find("rows")
                row = rows.find("row")
                return (row.get("LAST"))

    def __init__(self, ticker):
        self.ticker = ticker
        self.price = Stock.cur_price(self)


a = Stock('MGNT')
print(a.cur_price())