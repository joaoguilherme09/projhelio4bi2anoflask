# -*- coding: utf-8 -*-
from api.modelo.reserva import Reserva
from api.database.database import DatabaseConfig

"""
Representa o DAO (Data Access Object) de Reserva.

Objetivo:
- Encapsular operações de acesso a dados relacionadas à entidade Reserva.
- Permitir injeção de dependência do MysqlDatabase (que fornece conexões do pool).
"""
class ReservaDAO:
    def __init__(self, database_dependency: DatabaseConfig):
        """
        Construtor do DAO, recebe o Database (pool de conexões) por injeção de dependência.

        :param database_dependency: Instância de MysqlDatabase
        """
        print("⬆️ ReservaDAO.__init__()")
        self.__database = database_dependency  

    def create(self, objReserva: Reserva) -> int:
        SQL = "INSERT INTO reserva (idHospede, idHotel, inicio, fim) VALUES (%s, %s, %s, %s);"
        params = (objReserva.idHospede, objReserva.idHotel, objReserva.inicio, objReserva.fim)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                insert_id = cursor.lastrowid

                if not insert_id:
                    raise Exception("Falha ao inserir Reserva")
                
                print("✅ ReservaDAO.create()")
                return insert_id
            finally:
                cursor.close()
        finally:
            conn.close()

    def delete(self, reserva: Reserva) -> bool:
        SQL = "DELETE FROM reserva WHERE idReserva = %s;"
        params = (reserva.idReserva,)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount
                
                print("✅ ReservaDAO.delete()")
                return affected > 0
            finally:
                cursor.close()
        finally:
            conn.close()

    def update(self, objReserva: Reserva) -> bool:
        SQL = "UPDATE reserva SET idHospede = %s, idHotel = %s, inicio = %s, fim = %s WHERE idReserva = %s;"
        params = (objReserva.idHospede, objReserva.idHotel, objReserva.inicio, objReserva.fim, objReserva.idReserva)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(SQL, params)
                conn.commit()
                affected = cursor.rowcount
                
                print("✅ ReservaDAO.update()")
                return affected > 0
            finally:
                cursor.close()
        finally:
            conn.close()

    def findAll(self) -> list[dict]:
        SQL = "SELECT * FROM reserva;"

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(SQL)
                resultados = cursor.fetchall()
                
                print(f"✅ ReservaDAO.findAll() -> {len(resultados)} registros encontrados")
                return resultados
            finally:
                cursor.close()
        finally:
            conn.close()

    def findById(self, idReserva: int) -> dict | None:
        resultados = self.findByField("idReserva", idReserva)
        print("✅ ReservaDAO.findById()")
        return resultados[0] if resultados else None

    def findByField(self, field: str, value) -> list[dict]:
        allowed_fields = ["idReserva", "idHospede", "idHotel", "inicio", "fim"]
        if field not in allowed_fields:
            raise ValueError(f"Campo inválido para busca: {field}")

        SQL = f"SELECT * FROM reserva WHERE {field} = %s;"
        params = (value,)

        conn = self.__database.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(SQL, params)
                resultados = cursor.fetchall()
                
                print("✅ ReservaDAO.findByField()")
                return resultados
            finally:
                cursor.close()
        finally:
            conn.close()