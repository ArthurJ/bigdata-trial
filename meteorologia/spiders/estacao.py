from datetime import datetime
from functools import partial

import scrapy
from scrapy import signals

from lxml import etree as ET

from estacoes_dict import estacoes


class EstacaoSpider(scrapy.Spider):
    name = 'estacoes'

    def start_requests(self):
        for estacao, codigo in estacoes.items():
            yield scrapy.Request(
            f'https://www.saisp.br/geral/processo_cge.jsp?WHICHCHANNEL={codigo}',
            callback=partial(self.parse, estacao=estacao),
            headers={'referer': f'https://www.cgesp.org/v3/estacao.jsp?POSTO={codigo}'})
            # break

    def extract_table(self, body):
        colunas = []
        for th in ET.HTML(body).xpath('//th'):
            colunas.append(th.text)

        trs = ET.HTML(body).xpath("//tbody[@id='tbTelemBody']/tr")
        for tr in trs:
            linha = []
            linha.append(tr.getchildren()[0].text)
            for td in tr.getchildren()[1:]:
                linha.append(td.getchildren()[0]
                                .getchildren()[0]
                                .getchildren()[0].text)
            if linha:
                yield dict(zip(colunas, linha))

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
        for k, v in row.items():
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
