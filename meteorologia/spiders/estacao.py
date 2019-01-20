import json
import logging
from os import path
from datetime import datetime
from functools import partial
from itertools import cycle

from lxml import etree as ET

import scrapy
from scrapy import signals

from selenium import webdriver

from estacoes_dict import estacoes


class EstacaoSpider(scrapy.Spider):
    name = 'estacoes'

    def __init__(self, name=None, **kwargs):
        self.driver = webdriver.Firefox()

    def start_requests(self):
        for estacao, codigo in estacoes.items():
            yield scrapy.Request(
                    f'https://www.cgesp.org/v3/estacao.jsp?POSTO={codigo}',
                    callback=partial(self.parse, estacao=estacao))
        # yield scrapy.Request(
        #     f'https://www.cgesp.org/v3/estacao.jsp?POSTO={635}',
        #     callback=partial(self.parse, estacao='Pinheiros'))

    def extract_table(self, body):
        tables = ET.HTML(body).xpath('//body/table/tbody')

        colunas = []
        # linhas = []
        for table in tables:
            for tr in table.xpath('tr'):
                linha = []
                for th in tr.xpath('th'):
                    colunas.append(th.text) 
                for td in tr.xpath('td'):
                    if not td.text or (td.text != None and not td.text.strip()):
                        for i in td.xpath('table/tbody/tr/td'):
                            linha.append(i.text)
                            break
                    else:
                        linha.append(td.text.strip())
                if linha:
                    yield dict(zip(colunas, linha))

        # [print(l) for l in linhas]
        # return [dict(zip(colunas, linha)) for linha in linhas]

    def parse(self, response, estacao=''):
        for row in self.extract_table(response.body):
            yield {estacao: self.parse_row(row)}

    def parse_row(self, row):
        mapa_colunas = {'Chuva(mm)': 'chuva', 'Vel.VT(m/s)': 'vel_vento',
                        'Dir.VT(o)': 'dir_vento', 'Temp(oC)': 'temp',
                        'Umid.Rel.(%)': 'umidade', 'Pressão(mb)': 'pressao',
                        'Sens. Térmica(°C)': 'sens_termica',
                        'PressÃ£o(mb)': 'pressao', 'Data': 'timestamp'}
        parsed = dict()
        for k,v in row.items():
            v = v.strip()
            if not v:
                v = None
            elif k != 'Data':
                v = float(v)
            parsed[mapa_colunas[k]] = v if k != 'Data' else self.epoch(v)
        return parsed

    def epoch(self, timestamp):
        '''
            >>> est = EstacaoSpider()
            >>> est.epoch('18 JAN 2019 13:00')
            1547823600
            >>> est.spider_closed(est)
        '''
        # print(timestamp)
        meses = dict((zip(['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL',
                           'AGO', 'SET', 'OUT', 'NOV', 'DEZ'], range(1, 13))))
        t = timestamp.split(' ')
        t[1] = str(meses[t[1]])
        t = int(datetime.strptime(' '.join(t), '%d %m %Y %H:%M').timestamp())
        return t

    def spider_closed(self, spider):
        self.driver.close()
        self.driver.quit()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(EstacaoSpider, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider


if __name__ == '__main__':
    import doctest
    doctest.testmod()
