import json
import datetime

class Crud:

    def __init__(self,con):
        self.cur = con.cursor()
        self.con = con

        self.hashparse ={

            "nomeAlbum" : self._varchar,
            "dataAlbum" : self._varchar,
            "notaAlbum" : str,
            "Artista_idArtista" : str,
            "Formato_idFormato" : str,
            "Genero_idGenero" : str,

            "nomeMusica" : self._varchar,
            "notaMusica" : str,
            "duracaoMusica" : self._varchar,
            "Album_idAlbum" : str,
            "Artista_idArtista" : str,

            "nomeGenero" : self._varchar,

            "nomeArtista" : self._varchar,
            "dataArtista" : self._varchar,
            "Genero_idGenero" : str,

            "formatoNome" : self._varchar

        }
    
    def _varchar(self,string:str):
        return f"'{string}'"
    
    def _searchCheck(self,results:list,row_headers:list):
        results_list = list(results)
        parsed_result = list()
        for i in results_list:
            i = list(i)
            for j in i:
                if isinstance(j,datetime.date):
                    index = i.index(j)
                    i[index] = j.strftime("%Y-%m-%d")
                else:
                    index = i.index(j)
                    i[index] = str(j)
        
            parsed_result.append(dict(zip(row_headers,i)))
        jsonstring = json.dumps(parsed_result,indent=4, ensure_ascii=False).encode('utf-8')
        print(jsonstring.decode())
                    
                    

                

    def selectAll(self,table:str):
        """ SELECT * FROM -> table """

        query = "SELECT * FROM {}".format(table)
        self.cur.execute(query)
        row_headers=[x[0] for x in self.cur.description]
        results = self.cur.fetchall()
        self._searchCheck(results,row_headers)

    def selectWhere(self,table:str,whereConds:list,type=1):


        """| SELECT * FROM -> _table_ WHERE -> _list of conditions_ 
           | type= 1 -> AND cond 
             type= 2 -> OR cond |
        """



        query = "SELECT * FROM {} WHERE ".format(table)

        if len(whereConds) == 1:
            query = query + whereConds[0]
        else:
            for index,cond in enumerate(whereConds):
                if index == 0:
                    query = query + cond
                else:
                    if type == 1:
                        query = query + " AND " + cond
                    elif type == 2: 
                        query = query + " OR " + cond
                    else:
                        raise Exception("Wrong parameter on type AND/OR")
        
        self.cur.execute(query)
        row_headers=[x[0] for x in self.cur.description]
        results = self.cur.fetchall()
        self._searchCheck(results,row_headers)
            

    def insertOne(self, table:str, columns:list, values:list):
        """ INSERT INTO -> _table_ (_columnsList_) VALUES(_valuesList_)"""
        
        query = " INSERT INTO {}(".format(table)
        for index,column in enumerate(columns):
            if index != len(columns) - 1:
                query = query + column +","
            else:
                query = query + column
        query = query + ")"

        query = query + " VALUES("

        columns_values = tuple(zip(columns,values))

        aux = 1
        for column,value in columns_values:
            if aux != len(columns_values):
                action = self.hashparse.get(column)
                parsed_value = action(value)
                query = query + parsed_value + ","
                aux = aux + 1
            else:
                action = self.hashparse.get(column)
                parsed_value = action(value)
                query = query + parsed_value
        
        query = query + ")"

        self.cur.execute(query)
        self.con.commit()

        insert_id = self.cur.lastrowid

        print(f"New insertion on {table} with id: {insert_id}")


    def updateWhere(self,table:str,columns:list,values:list,whereConds:list,type=1):
        """ | UPDATE -> _table_ SET -> _columns_ = _values_ WHERE -> _whereConds_
            | type= 1 -> AND cond 
              type= 2 -> OR cond |
        """

        query = "UPDATE {} SET ".format(table)

        columns_values = tuple(zip(columns,values))
        aux = 1
        for column,value in columns_values:
            if aux != len(columns_values):
                action = self.hashparse.get(column)
                parsed_value = action(value)
                query = query + "{} = {}, ".format(column,parsed_value)
                aux = aux + 1
            else: 
                action = self.hashparse.get(column)
                parsed_value = action(value)
                query = query + "{} = {} ".format(column,parsed_value)
        
        query = query +"WHERE "
        if len(whereConds) == 1:
            query = query + whereConds[0]
        else:
            for index,cond in enumerate(whereConds):
                if index == 0:
                    query = query + cond
                else:
                    if type == 1:
                        query = query + " AND " + cond
                    elif type == 2: 
                        query = query + " OR " + cond
                    else:
                        raise Exception("Wrong parameter on type AND/OR")
        
        self.cur.execute(query)
        self.con.commit()

        records_affected = self.cur.rowcount

        print(records_affected," rows affected")

    def deleteWhere(self, table:str, whereConds:list, type = 1):
        query = "DELETE FROM {} WHERE ".format(table)
        if len(whereConds) == 1:
            query = query + whereConds[0]
        else:
            for index,cond in enumerate(whereConds):
                if index == 0:
                    query = query + cond
                else:
                    if type == 1:
                        query = query + " AND " + cond
                    elif type == 2: 
                        query = query + " OR " + cond
                    else:
                        raise Exception("Wrong parameter on type AND/OR")
        
        self.cur.execute(query)
        self.con.commit()

        records_affected = self.cur.rowcount

        print(records_affected," rows affected")


    def call_sp(self,proc:str,args:str):
        args = [args]
        self.cur.callproc(proc,args)
        for s_r in self.cur.stored_results():
            row_headers=[x[0] for x in s_r.description]
            results = s_r.fetchall()
        self._searchCheck(results,row_headers)


            
    def close(self):
        self.cur.close()
        self.con.close()

