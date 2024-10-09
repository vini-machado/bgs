# Gerador de Relatórios - B280 (BGS)

## Objetivo
Este repositório contém o código-fonte de uma ETL em Python, que consome informações do banco de dados do BGS e pré-preenche algumas informações do ensaio realizado, por meio de uma caixa de diálogo.

## Condições de contorno
1) O código precisa rodar no sistema operacional Windows.
2) Instalação de [Python >= 3.11](https://www.python.org/downloads/).
3) Instalação do driver compatível com `Microsoft Access Driver (*.mdb, *.accdb)`, que pode ser baixado no [site da Microsoft](https://www.microsoft.com/pt-br/download/details.aspx?id=54920).
4) Com um terminal aberto dentro da pasta `bgs/`, rodar:
```
pip install -r requirements.txt
```

## Estrutura de código
```
src/
    ├── config/
    ├── queries/
    ├── utils/
    ├── main.py
    ├── run.bat
    └── run.vbs
```

- **config/**: reúne configurações básicas da ETL, como, por exemplo, conexão com o banco de dados.
- **queries/**: reúne os arquivos em SQL responsáveis pela consulta ao banco de dados.
    - O BGS usa o banco de dados MDB.
- **utils/**: reúne arquivos que executam funções diversas dentro da aplicação.
    - `gui.py`: GUI significa _Graphical User Interface_. Esse arquivo é responsável pela geração dos elementos gráficos da caixa de diálogo. Para adicionar novos campos, basta adicionar novos elementos na lista de fields em `self.formdata` (mantenha o padrão!!!)     
    - `measurement.py`: arquivo responsável pela extração e transformação dos dados no banco de dados MDB e dos arquivos `rowdata` da pasta `rough_data`.
    - `report.py`: arquivo responsável pela geração do relatório, substituindo as informações colhidas no arquivo `gui.py` e criando uma página com os dados extraídos no arquivo `measurement.py`.
- **main.py**: arquivo central que inicia todo o processo.
- **run.bat** e **run.vbs**: arquivos executáveis.
