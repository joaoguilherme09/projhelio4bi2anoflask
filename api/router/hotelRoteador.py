# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.hotelMiddleware import HotelMiddleware
from api.controle.hotelControl import HotelControl

class HotelRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Hotel no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Hotel.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, Hotel_middleware: HotelMiddleware, Hotel_control: HotelControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param Hotel_middleware: Middleware com validações específicas para Hotel (ex.: validação de corpo, id).
        :param Hotel_control: Controlador que implementa a lógica de negócio (store, index, update, delete, show).

        Observações:
        - Blueprint é criado para permitir o registro isolado de rotas.
        - Injeção de dependência garante desacoplamento: o roteador não precisa criar middlewares ou controlador.
        """
        print("⬆️  HotelRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__Hotel_middleware = Hotel_middleware
        self.__Hotel_control = Hotel_control

        # Blueprint é a coleção de rotas da entidade Hotel
        self.__blueprint = Blueprint('Hotel', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Hotel.

        Rotas implementadas:
        - POST /        -> Cria um novo Hotel
        - GET /         -> Lista todos os Hoteis
        - GET /<id>     -> Retorna um Hotel por ID
        - PUT /<id>     -> Atualiza um Hotel por ID
        - DELETE /<id>  -> Remove um Hotel por ID

        Observações:
        - Cada rota aplica autenticação JWT.
        - Middlewares de validação são aplicados diretamente.
        - Para rotas que precisam do idHotel, o parâmetro vem da URI.
        """

        # POST / -> cria um Hotel
        @self.__blueprint.route('/', methods=['POST'])
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__Hotel_middleware.validate_body  # valida corpo da requisição
        def store():
            """
            Rota responsável por criar um novo Hotel.
            O corpo da requisição deve conter os dados do Hotel validados pelo middleware.
            """
            return self.__Hotel_control.store()

        # GET / -> lista todos os Hoteis
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os Hoteis cadastrados no sistema.
            """
            return self.__Hotel_control.index()

        # GET /<idHotel> -> retorna um Hotel específico
        @self.__blueprint.route('/<int:idHotel>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__Hotel_middleware.validate_id_param  # valida se o ID é válido
        def show(idHotel):
            """
            Rota que retorna um Hotel específico pelo seu ID.

            :param idHotel: int - ID do Hotel vindo da URI.
            """
            return self.__Hotel_control.show()

        # PUT /<idHotel> -> atualiza um Hotel
        @self.__blueprint.route('/<int:idHotel>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__Hotel_middleware.validate_id_param
        @self.__Hotel_middleware.validate_body
        def update(idHotel):
            """
            Rota que atualiza um Hotel existente.

            Observações:
            - idHotel vem da URI (request.view_args['idHotel']).
            - Corpo da requisição validado pelo middleware validate_body.
            """
            return self.__Hotel_control.update()

        # DELETE /<idHotel> -> remove um Hotel
        @self.__blueprint.route('/<int:idHotel>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__Hotel_middleware.validate_id_param
        def destroy(idHotel):
            """
            Rota que remove um Hotel pelo seu ID.

            :param idHotel: int - ID do Hotel a ser removido.
            """
            return self.__Hotel_control.destroy()

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint