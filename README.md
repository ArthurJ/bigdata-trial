# Crawling

O código precisa ser executado usando Python 3.7+

### Instalando pacotes necessários
`$ pip install -r requirements.txt`

Pacotes usados:
- Scrapy
- Selenium 

O Webdriver do Firefox precisa estar disponível no PATH.
Download em https://github.com/mozilla/geckodriver/releases/tag/v0.23.0

### Executando:

`$ scrapy crawl estacoes`

Os resultados serão escritos no arquivo `resultados.json`

---

### Crawleando as estações meteorológicas de São Paulo

Neste desafio você deverá obter os dados das estações meteorológicas de São Paulo através do site: https://www.cgesp.org/v3/estacoes-meteorologicas.jsp . Seu crawler deverá retornar um objeto JSON contendo os seguintes dados de todas as estações meteorológicas nas últimas 24 horas: timestamp (convertido para epoch), chuva, velocidade do vento, direção do vento, temperatura, umidade relativa e pressão.

### Exemplo de resultado esperado do crawler:
```
{
  "Penha": [
    {
        "timestamp": 1542632400,
        "chuva": 1.2,
        "vel_vento": 3.01,
        "dir_vento": 8,
        "temp": 17.51,
        "umidadade_rel": 86.92,
        "pressao": 934.55
    },
    {
        "timestamp": 1542628800,
        "chuva": 1,
        "vel_vento": 0,
        "dir_vento": 26,
        "temp": 18.04,
        "umidadade_rel": 86.77,
        "pressao": 933.98
    }, 
    ... 
  ],
  "Perus": [
    {
        "timestamp": 1542632400,
        "chuva": 4,
        "vel_vento": 0.19,
        "dir_vento": 136,
        "temp": 18.22,
        "umidadade_rel": 92.31,
        "pressao": 929.58
    },
    {
        "timestamp": 1542628800,
        "chuva": 3.6,
        "vel_vento": 0,
        "dir_vento": 243,
        "temp": 17.84,
        "umidadade_rel": 93.14,
        "pressao": 929.56
    }, 
    ... 
  ],
  ...
}
```
