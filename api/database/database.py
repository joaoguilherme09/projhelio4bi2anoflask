import mysql.connector                # biblioteca mysql-connector-python
from mysql.connector import pooling   # pooling serve para gerenciamento de conexões
import sys                            # sys para manipulação de saída de erro

class DatabaseConfig:
        __pool = None

        # cria o construtor com os parâmetros de conexão
        def __init__(
                    self,
                    pool_name="mypool",
                    pool_size=25,
                    pool_reset_session=True,
                    host="127.0.0.1",
                    user="root",
                    password="",
                    database="casa_branca",
                    port=3306
                    ):
            
        # inicializa os atributos da classe
                self.pool_name = pool_name
                self.pool_size = pool_size
                self.pool_reset_session = pool_reset_session
                self.host = host
                self.user = user
                self.database = database
                self.port = port
        
        # método para conectar ao banco de dados
        def connect(self):
                if DatabaseConfig.__pool is None: # se ainda não for estabelecida uma conexão, cria uma nova
                        try:
                            DatabaseConfig.__pool = mysql.connector.pooling.MySQLConnectionPool(
                                pool_name=self.pool_name,
                                pool_size=self.pool_size,
                                pool_reset_session=self.pool_reset_session,
                                host=self.host,
                                user=self.user,              
                                database=self.database,
                                port=self.port,
                                auth_plugin='mysql_native_password'
                            )
                            conn = DatabaseConfig.__pool.get_connection()  # testa a conexão
                            print("⬆️  Conectado ao MySQL com sucesso!")
                            conn.close()                                   # Libera a conexão de teste
                        except mysql.connector.Error as err:
                            print(f"❌ Falha ao conectar ao MySQL: {err}")
                            sys.exit(1)
                return DatabaseConfig.__pool
            
        def get_connection(self):
            pool = self.connect()
            return pool.get_connection()