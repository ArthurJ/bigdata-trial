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

### Perguntas e Respostas

    - O que você faria caso quisesse obter essas informações de forma recorrente, ou seja, todo dia?
        Como eu desenvolvi a solução usando Scrapy, poderia usar o Sprapyhub para executar automaticamente a ingestão dos dados. Outra possibilidade seria usar o Airflow ou o (mais simples e menos resiliente) Crontab.

    - Como você validaria se as respostas obtidas do crawler estão corretas ou não?
        * Verificar se a estrutura do site se manteve a mesma em que me baseei no desenvolvimento da solução.
        * Verificar se os dados são do tipo esperado, e se estão dentro de uma faixa esperada (São Paulo dificilmente teria valores negativos, por exemplo)
        * Buscar em outras fontes os mesmos valores e verificar se os resultados são semelhantes

    - O que você faria se tivesse mais tempo para resolver o desafio?
        Escolhi usar o Selenium para acessar os endereços devido a presença do iframe na página contendo a tabela com as informações, o que implica em processar javascript, o que o Scrapy sozinho não seria capaz de fazer. A vantagem do Selenium é sua versatilidade, porém, na configuração atual o Selenium é um gargalo para o Scrapy, por não permitir o acesso as páginas de modo concorrente que o Scrapy sozinho faria. Se o número de páginas a serem acessadas fosse muito maior do que o proposto no exercício, usar o Selenium combinado com Docker para trabalho em paralelo, ou substituir o Selenium por uma outra solução compatível com o Scrapy capaz de acessar os dados do iframe seria um bom investimento de tempo.
        Outras opções para melhorar essa implementação poderia ser armazenar os dados e/ou criar um dashboard para visualização, mas isso depende do que traria mais valor ao projeto.

    - Como você resolveria esse desafio e/ou as perguntas caso tivesse acesso aos recursos da Amazon Web Services, Azure ou Google Cloud?
        Além do que já citei, armazenamento dos dados na núvem, disponilizar uma API para acessa-los.
