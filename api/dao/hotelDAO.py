# -*- coding: utf-8 -*-
from api.modelo.hotel import Hotel
from api.database.database import DatabaseConfig

"""
Representa o DAO (Data Access Object) de Hotel.

Objetivo:
- Encapsular operações de acesso a dados relacionadas à entidade Hotel.
- Permitir injeção de dependência do MysqlDatabase (que fornece conexões do pool).
"""
class HotelDAO:
    def __init__(self, database_dependency: DatabaseConfig):
        """
        Construtor do DAO, recebe o Database (pool de conexões) por injeção de dependência.

        :param database_dependency: Instância de MysqlDatabase
        """
        print("⬆️ HotelDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objHotel: Hotel) -> int:
        SQL = "INSERT INTO hotel (nome,capacidade) VALUES (%s,%s);"
        params = (objHotel.nome,objHotel.capacidade)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

                if not insert_id:
                    raise Exception("Falha ao inserir Hotel")
                
                print("✅ HotelDAO.create()")
                return insert_id
            finally:
                cursor.close()
        finally:
            conn.close()

    def delete(self, Hotel: Hotel) -> bool:
        SQL = "DELETE FROM hotel WHERE idHotel = %s;"
        params = (Hotel.idHotel,)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount
                
                print("✅ HotelDAO.delete()")
                return affected > 0
            finally:
                cursor.close()
        finally:
            conn.close()

    def update(self, objHotel: Hotel) -> bool:
        SQL = "UPDATE Hotel SET nome = %s, capacidade = %s WHERE idHotel = %s;"
        params = (objHotel.nome, objHotel.capacidade, objHotel.idHotel)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount
                
                print("✅ HotelDAO.update()")
                return affected > 0
            finally:
                cursor.close()
        finally:
            conn.close()

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM hotel;"

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(SQL)
                resultados = cursor.fetchall()
                
                print(f"✅ HotelDAO.findAll() -> {len(resultados)} registros encontrados")
                return resultados
            finally:
                cursor.close()
        finally:
            conn.close()

    def findById(self, idHotel: int) -> dict | None:
        resultados = self.findByField("idHotel", idHotel)
        print("✅ HotelDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idHotel", "nome", "capacidade"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM hotel WHERE {field} = %s;"
        params = (value,)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()
                
                print("✅ HotelDAO.findByField()")
                return resultados
            finally:
                cursor.close()
        finally:
            conn.close()