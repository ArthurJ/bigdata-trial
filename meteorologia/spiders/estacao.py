import json
import logging
from os import path
from datetime import datetime
from functools import partial

import scrapy
from scrapy import signals

from estacoes_dict import estacoes

from selenium import webdriver


class EstacaoSpider(scrapy.Spider):
    name = 'estacoes'

    def __init__(self, name=None, **kwargs):
        self.driver = webdriver.Firefox()
    
    def start_requests(self):
        for estacao, codigo in estacoes.items():
            yield scrapy.Request(
                    f'https://www.cgesp.org/v3/estacao.jsp?POSTO={codigo}',
                    callback=partial(self.parse, estacao=estacao))

    def parse(self, response, estacao=''):
        self.driver.get(response.url)
        self.driver.switch_to.frame('frm-historico')
        
        table_rows = self.driver.find_elements_by_xpath('//*[@id="tbDadosTelem"]//tr')
        
        linhas = []
        colunas = self.build_colunas(table_rows[0].text)

        for row in table_rows[1:]:
            text = row.text.split('\n')
            if len(text) > 1:
                if len(text) == len(colunas) + 1:
                    item = dict(zip(['timestamp'] + colunas, text))
                    item['timestamp'] = self.epoch(item['timestamp'])
                    for key in colunas:
                        item[key] = float(item[key])
                    linhas.append(item)
                else:
                    self.log(
                        f'\n\tEstação: {estacao}'+
                        f'\n\tLinha inconsistente: {text}' +
                        f'\n\tEndereço: {response.url}'+
                        f'\n\tColunas esperadas:{["Data"] + colunas}\n\n',
                        logging.ERROR)
        yield {estacao:linhas}

    def build_colunas(self, header_line):
        mapa_colunas = {'Chuva(mm':'chuva', 'Vel.VT(m/s':'vel_vento',
                        'Dir.VT(o':'dir_vento', 'Temp(oC':'temp', 
                        'Umid.Rel.(%':'umidade', 'Pressão(mb':'pressao', 
                        'Sens. Térmica(°C':'sens_termica', 
                        'PressÃ£o(mb':'pressao'}
        
        header = header_line[5:]
        return [mapa_colunas[c.strip()] 
                    for c in header.split(')') if c.strip()]

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
    
