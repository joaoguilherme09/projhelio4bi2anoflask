# -*- coding: utf-8 -*-
from api.modelo.hospede import Hospede
from api.database.database import DatabaseConfig

"""
Representa o DAO (Data Access Object) de Hospede.

Objetivo:
- Encapsular operações de acesso a dados relacionadas à entidade Hospede.
- Permitir injeção de dependência do MysqlDatabase (que fornece conexões do pool).
"""
class HospedeDAO:
    def __init__(self, database_dependency: DatabaseConfig):
        """
        Construtor do DAO, recebe o Database (pool de conexões) por injeção de dependência.

        :param database_dependency: Instância de MysqlDatabase
        """
        print("⬆️ HospedeDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objHospede: Hospede) -> int:
        SQL = "INSERT INTO hospede (nome,email,telefone,requisicao,cpf) VALUES (%s,%s,%s,%s,%s);"
        params = (objHospede.nomeHospede,objHospede.email,objHospede.telefone,objHospede.requisicao,objHospede.cpf)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

                if not insert_id:
                    raise Exception("Falha ao inserir Hospede")
                
                print("✅ HospedeDAO.create()")
                return insert_id
            finally:
                cursor.close()
        finally:
            conn.close()

    def delete(self, Hospede: Hospede) -> bool:
        SQL = "DELETE FROM hospede WHERE idHospede = %s;"
        params = (Hospede.idHospede,)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount
                
                print("✅ HospedeDAO.delete()")
                return affected > 0
            finally:
                cursor.close()
        finally:
            conn.close()

    def update(self, objHospede: Hospede) -> bool:
        SQL = "UPDATE hospede SET nome = %s, email = %s, telefone = %s, requisicao = %s, cpf = %s WHERE idHospede = %s;"
        params = (objHospede.nomeHospede,objHospede.email, objHospede.telefone, objHospede.requisicao, objHospede.cpf, objHospede.idHospede)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount
                
                print("✅ HospedeDAO.update()")
                return affected > 0
            finally:
                cursor.close()
        finally:
            conn.close()

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM hospede;"

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(SQL)
                resultados = cursor.fetchall()
                
                print(f"✅ HospedeDAO.findAll() -> {len(resultados)} registros encontrados")
                return resultados
            finally:
                cursor.close()
        finally:
            conn.close()

    def findById(self, idHospede: int) -> dict | None:
        resultados = self.findByField("idHospede", idHospede)
        print("✅ HospedeDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idHospede", "nome", "email", "telefone", "requisicao", "cpf"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM hospede WHERE {field} = %s;"
        params = (value,)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()
                
                print("✅ HospedeDAO.findByField()")
                return resultados
            finally:
                cursor.close()
        finally:
            conn.close()