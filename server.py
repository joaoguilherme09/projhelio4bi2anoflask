from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from werkzeug.exceptions import HTTPException, NotFound

from api.database.database import DatabaseConfig
from api.utils.errorResponse import ErrorResponse
from api.utils.logger import Logger

# Middlewares
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.hospedeMiddleware import HospedeMiddleware
from api.Middleware.hotelMiddleware import HotelMiddleware
from api.Middleware.reservaMiddleware import ReservaMiddleware

# Controls
from api.controle.hospedeControl import HospedeControl
from api.controle.hotelControl import HotelControl
from api.controle.reservaControl import ReservaControl

# Services
from api.service.hospedeService import HospedeService
from api.service.hotelService import HotelService
from api.service.reservaService import ReservaService

# DAOs
from api.dao.hospedeDAO import HospedeDAO
from api.dao.hotelDAO import HotelDAO
from api.dao.reservaDAO import ReservaDAO
from api.dao.usuariosDAO import UsuarioDAO


# Routers
from api.router.hospedeRoteador import HospedeRoteador
from api.router.hotelRoteador import HotelRoteador
from api.router.reservaRoteador import ReservaRoteador
from api.router.authRoteador import AuthRoteador

import traceback


class Server:
    """
    Classe principal do servidor Flask.

    Responsável por inicializar middlewares, roteadores e gerenciar a aplicação.
    """

    def __init__(self, porta: int = 8000):
        # 🔹 Porta em que o servidor irá rodar
        self.__porta = porta

        # 🔹 Instância Flask, configurando pasta de arquivos estáticos
        self.__app = Flask(__name__, static_folder="static", static_url_path="")

        # 🔹 Configuração de CORS (Cross-Origin Resource Sharing)
        #    Permite que clientes de outros domínios/portas acessem sua API
        #    Exemplo: permitir todos os domínios (somente para desenvolvimento)
        # 🔹 Configuração de CORS (Cross-Origin Resource Sharing)
#    Permite que frontend acesse a API de forma controlada
        CORS(self.__app, 
            origins=[
                "http://localhost", 
                "http://127.0.0.1:8000", 
                "http://localhost:5500", 
                "http://127.0.0.1:5500",
                "http://localhost:3000",
                "http://127.0.0.1:3000"
            ],
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            allow_headers=[
                "Content-Type", 
                "Authorization", 
                "X-Requested-With",
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Headers",
                "Access-Control-Allow-Methods"
            ],
            supports_credentials=True,
            expose_headers=["Content-Range", "X-Content-Range"],
            max_age=3600)

        # 🔹 Middlewares
        self.__jwt_middleware = JwtMiddleware()
        self.__hospede_middleware = HospedeMiddleware()
        self.__hotel_middleware = HotelMiddleware()
        self.__reserva_middleware = ReservaMiddleware()

        # 🔹 DAOs, Services e Controls serão inicializados após conexão com DB
        self.__hospede_dao = None
        self.__hotel_dao = None
        self.__reserva_dao = None
        self.__hospede_service = None
        self.__hotel_service = None
        self.__reserva_service = None
        self.__hospede_control = None
        self.__hotel_control = None
        self.__reserva_control = None
        self.__usuario_dao = None
        

        # 🔹 Conexão global com o banco
        self.__db_connection = None

    def init(self):
        """
        Inicializa a aplicação:
        - Conexão com o banco
        - Middlewares
        - Roteadores
        """
        # Middleware para parsing JSON já é nativo do Flask
        # Middleware para arquivos estáticos já configurado na criação do Flask

        # 🔹 Middleware de log antes das rotas
        self.__before_routing()

        # 🔹 Conexão global com MySQL (injeção de dependência)
        self.__db_connection = DatabaseConfig(
            pool_name="mypool",
            pool_size=10,
            host="127.0.0.1",
            user="root",
            password="Henry45*1",
            database="casa_branca",
            port=3306
        )

        self.__db_connection.connect()

        # 🔹 Configuração do módulo Hospede
        self.__setup_hospede()

        # 🔹 Configuração do módulo Hotel
        self.__setup_hotel()

        # 🔹 Configuração do módulo Reserva
        self.__setup_reserva()

        # 🔹 Configuração do módulo Aut
        self.__setup_auth()

        # 🔹 Middleware global de tratamento de erros
        self.__error_middleware()

    def __setup_hospede(self):
        """Configura o módulo Hospede (DAO, Service, Control, Router)"""
        print("⬆️  Setup Hospede")

        # DAO recebe conexão global com o banco (injeção de dependência)
        self.__hospede_dao = HospedeDAO(self.__db_connection)

        # Service recebe DAO (injeção de dependência)
        self.__hospede_service = HospedeService(self.__hospede_dao)

        # Controller recebe Service (injeção de dependência)
        self.__hospede_control = HospedeControl(self.__hospede_service)

        # Router recebe Controller + Middlewares
        hospede_router = HospedeRoteador(
            self.__jwt_middleware,
            self.__hospede_middleware,
            self.__hospede_control
        )

        # Registra rotas da entidade Hospede
        self.__app.register_blueprint(hospede_router.create_routes(), url_prefix="/api/v1/hospedes")

    def __setup_hotel(self):
        """Configura o módulo Hotel (DAO, Service, Control, Router)"""
        print("⬆️  Setup Hotel")

        # DAO recebe conexão global com o banco (injeção de dependência)
        self.__hotel_dao = HotelDAO(self.__db_connection)

        # Service recebe DAO via injeção de dependência
        self.__hotel_service = HotelService(self.__hotel_dao)

        # Controller recebe Service
        self.__hotel_control = HotelControl(self.__hotel_service)

        # Router recebe Controller + Middlewares
        hotel_router = HotelRoteador(
            self.__jwt_middleware,
            self.__hotel_middleware,
            self.__hotel_control
        )

        # Registra rotas da entidade Hotel
        self.__app.register_blueprint(hotel_router.create_routes(), url_prefix="/api/v1/hoteis")

    def __setup_reserva(self):
        """Configura o módulo Reserva (DAO, Service, Control, Router)"""
        print("⬆️  Setup Reserva")

        # DAO
        self.__reserva_dao = ReservaDAO(self.__db_connection)

        # garante DAOs dependentes
        if self.__hospede_dao is None:
            self.__hospede_dao = HospedeDAO(self.__db_connection)
        if self.__hotel_dao is None:
            self.__hotel_dao = HotelDAO(self.__db_connection)

        # Service
        self.__reserva_service = ReservaService(self.__reserva_dao, self.__hospede_dao, self.__hotel_dao)

        # Controller
        self.__reserva_control = ReservaControl(self.__reserva_service)

        # Router
        reserva_router = ReservaRoteador(
            self.__jwt_middleware,
            self.__reserva_middleware,
            self.__reserva_control
        )
        self.__app.register_blueprint(reserva_router.create_routes(), url_prefix="/api/v1/reservas")

    def __setup_auth(self):
        """Configura autenticação"""
        print("⬆️  Setup Auth")
        auth_router = AuthRoteador(self.__db_connection)  # Passa conexão
        self.__app.register_blueprint(auth_router.create_routes(), url_prefix="/api/v1/auth")

    def __before_routing(self):
        """Middleware que loga separador antes de cada requisição"""
    
        # 🔥 NOVAS ROTAS PARA SERVIR OS ARQUIVOS HTML
        @self.__app.route('/Hospedes.html')
        def serve_hospedes():
            print("📄 Servindo Hospedes.html")
            return send_from_directory(self.__app.static_folder, 'Hospedes.html')
        
        @self.__app.route('/Hoteis.html')
        def serve_hoteis():
            print("📄 Servindo Hoteis.html")
            return send_from_directory(self.__app.static_folder, 'Hoteis.html')
        
        @self.__app.route('/Reservas.html')
        def serve_reservas():
            print("📄 Servindo Reservas.html")
            return send_from_directory(self.__app.static_folder, 'Reservas.html')
        
        @self.__app.route('/dashboard.html')
        def serve_dashboard():
            print("📄 Servindo dashboard.html")
            return send_from_directory(self.__app.static_folder, 'dashboard.html')

        @self.__app.before_request
        def log_separator():
            print("-" * 70)

        # rota para servir a página de login na raiz '/'
        @self.__app.route('/', methods=['GET'])
        def serve_root():
            # envia o arquivo static/login.html
            return send_from_directory(self.__app.static_folder, 'login.html')

    def __error_middleware(self):
        """Middleware global de tratamento de erros"""
        @self.__app.errorhandler(Exception)
        def handle_error(error):
           

            # 🔹 404 - Rota ou arquivo não encontrado
            if isinstance(error, NotFound):
                return error, 404

            # 🔹 Captura ErrorResponse customizado
            if isinstance(error, ErrorResponse):
                print("🟡 Server.error_middleware()")
                # Extrai stack trace como string
                stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))

                Logger.log_error(error)  # Loga a exceção real

                resposta = {
                    "success": False,
                    "error": {
                        "message": str(error),
                        "code": getattr(error, "code", None),
                        "details": getattr(error, "error", None)
                    },
                    "data": {
                        "message": "Erro tratado pela aplicação",
                        "stack": stack_str
                    }
                }
                return jsonify(resposta), error._httpCode

            # 🔹 Outros erros internos (não tratados)
            stack_str = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            print("🟡 Server.error_middleware()")
            resposta = {
                "success": False,
                "error": {
                    "message": str(error),
                    "code": getattr(error, "code", None)
                },
                "data": {
                    "message": "Ocorreu um erro interno no servidor",
                    "stack": stack_str
                }
            }

            Logger.log_error(error)  # Loga a exceção real
            return jsonify(resposta), 500

    def run(self):
        """Inicia o servidor Flask na porta configurada"""
        print(f"🚀 Servidor rodando em: http://127.0.0.1:{self.__porta}")
        # ⚠️ debug=False é necessário para que o errorhandler global capture exceções
        self.__app.run(port=self.__porta, debug=False)
