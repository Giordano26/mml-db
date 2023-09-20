import mysql.connector
from CRUD import Crud

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MariaxD12@",
    database="mydb"
)

op = Crud(connection)

op.call_sp('sp_albumcompleto','queen')

op.close()



