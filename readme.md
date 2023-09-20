# CRUD - My Music List Doc 

## Instalação 

`$ pip install mysql-connector-python` <p> instalação do conector do mysql para python


# Iniciando conector

```py
import mysql.connector
from CRUD import Crud

#substitua os parâmetros pelos parâmetros do seu banco de dados
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root", 
    database="mydb"
)

```

iniciar objeto da conexão para chamada dos métodos:

```py
op = Crud(connection)

```

após realização dos métodos desejados, sempre encerrar a conexão como no seguinte exemplo:

```py
op = Crud(connection) #instancia o objeto

op.selectAll("Album") #chamada de método

op.close() #encerra a conexão com o banco de dados

``` 
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

## Operações

* Select All -> `SELECT * FROM table`
<p>


| Parâmetro   | Tipo   | Descrição            | Obrigatório |
|-------------|--------|----------------------|-------------|
| `table`     | string | nome da tabela       | Obrigatório |

exemplo:
```py
op.selectAll("Album")
```

resposta:
```json
{
        "idAlbum": "3",
        "nomeAlbum": "Siamese Dream",
        "dataAlbum": "1993-07-27",
        "notaAlbum": "10.00",
        "Artista_idArtista": "4",
        "Formato_idFormato": "2",
        "Genero_idGenero": "4"
},
...
```
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

* Select Where -> `SELECT * FROM table WHERE conditions (AND/OR)`

<p>


| Parâmetro   | Tipo   | Descrição            | Obrigatório |
|-------------|--------|----------------------|-------------|
| `table`      | string | nome da tabela       | Obrigatório |
| `conditions` | list | lista de condições     | Obrigatório |
| `type`       | int | 1 -> AND / 2 -> OR      | Opcional, 1 por padrão |

exemplo:
```py
op.selectWhere("Album",["idAlbum = 3","idAlbum = 2"],type=2)
```
resposta:

```json
{
        "idAlbum": "2",
        "nomeAlbum": "Hatful of Hollow",
        "dataAlbum": "1984-11-12",
        "notaAlbum": "10.00",
        "Artista_idArtista": "3",
        "Formato_idFormato": "1",
        "Genero_idGenero": "3"
    },
    {
        "idAlbum": "3",
        "nomeAlbum": "Siamese Dream",
        "dataAlbum": "1993-07-27",
        "notaAlbum": "10.00",
        "Artista_idArtista": "4",
        "Formato_idFormato": "2",
        "Genero_idGenero": "4"
    }
```
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

* insert one -> `INSERT INTO table(columnsList) VALUES(valuesList)`

<p>

| Parâmetro   | Tipo   | Descrição            | Obrigatório |
|-------------|--------|----------------------|-------------|
| `table`      | string | nome da tabela       | Obrigatório |
| `columns` | list | lista de colunas     | Obrigatório |
| `values`       | list | lista de valores      | Obrigatório |


exemplo:

```py
op.insertOne("Musica",
            ["nomeMusica","notaMusica","duracaoMusica","Album_idAlbum","Artista_idArtista"],
            ["Kerosene",10.0,"00:03:12",7,6])
```

resposta:
```bash
New insertion on Musica with id: 50
```
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

- Update Where -> `UPDATE table SET columns = values WHERE conditions`
<p>

| Parâmetro   | Tipo   | Descrição            | Obrigatório |
|-------------|--------|----------------------|-------------|
| `table`      | string | nome da tabela       | Obrigatório |
| `columns` | list | lista de colunas     | Obrigatório |
| `values`       | list | lista de valores      | Obrigatório |
| `conditions` | list | lista de condições     | Obrigatório |
| `type`       | int | 1 -> AND / 2 -> OR      | Opcional, 1 por padrão |

exemplo:
```py
op.updateWhere("Musica",["notaMusica"],
             [8.5],
             ['idMusica = 50'])
```
resposta:
```bash
1 rows affected
```
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

- Delete Where -> `DELETE FROM table WHERE conditions`
<p>

| Parâmetro   | Tipo   | Descrição            | Obrigatório |
|-------------|--------|----------------------|-------------|
| `table`      | string | nome da tabela       | Obrigatório |
| `conditions` | list | lista de condições     | Obrigatório |
| `type`       | int | 1 -> AND / 2 -> OR      | Opcional, 1 por padrão |

exemplo:
```py
op.deleteWhere("Musica",['idMusica = 50'],type=1)
```
resposta:
```bash
1 rows affected
```
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

- Call Stored Procedure -> ```CALL sp(params)```
<p>

| Parâmetro   | Tipo   | Descrição            | Obrigatório |
|-------------|--------|----------------------|-------------|
| `proc`      | string | nome da stored procedure       | Obrigatório |
| `args` | string | argumentos da stored procedure     | Obrigatório |

exemplo:
```py
op.call_sp('sp_albumresumo','dream')
```

resposta:

```json
{
        "Album": "Siamese Dream",
        "Artista": "The Smashing Pumpkins",
        "Data": "1993-07-27",
        "Numero de faixas": "13",
        "Duração": "1:02:09",
        "Formato": "Digital",
        "Genero": "Grunge"
}
```
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

## Relatórios (Stored Procedures)

My Music List atualmente conta com dois relatórios prontos, um para resumo do album e um para informações completas sobre o album.<p>
Ambas buscas são realizadas pelo nome do álbum, como no exemplo a seguir

exemplo:
```py
op.call_sp('sp_albumresumo','dream')
```

resposta:
```json
{
        "Album": "Siamese Dream",
        "Artista": "The Smashing Pumpkins",
        "Data": "1993-07-27",
        "Numero de faixas": "13",
        "Duração": "1:02:09",
        "Formato": "Digital",
        "Genero": "Grunge"
}
```

<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

exemplo:
```py
op.call_sp('sp_albumcompleto','queen')
```

resposta: 
```json
{
        "Artista": "The Smiths",
        "Album": "The Queen is Dead",
        "Genero": "Post-Punk",
        "Formato": "Vinil",
        "Ano": "1986-06-16",
        "Nota Album": "10.00",
        "Duração Album": "0:37:08",
        "Numero de Faixas": "10",
        "Faixa": "The Queen is Dead",
        "Duração Faixa": "0:06:25",
        "Nota Faixa": "None"
    },
    {
        "Artista": "The Smiths",
        "Album": "The Queen is Dead",
        "Genero": "Post-Punk",
        "Formato": "Vinil",
        "Ano": "1986-06-16",
        "Nota Album": "10.00",
        "Duração Album": "0:37:08",
        "Numero de Faixas": "10",
        "Faixa": "Frankly, Mr. Shankly",
        "Duração Faixa": "0:02:19",
        "Nota Faixa": "None"
    },
...
```
<div style="page-break-after: always; visibility: hidden">
\pagebreak
</div>

## Dependências
* [My Sql Connector](https://dev.mysql.com/doc/connector-python/en/)

* [My Sql Server](https://dev.mysql.com/downloads/mysql/)
