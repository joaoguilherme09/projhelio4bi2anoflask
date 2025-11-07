# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.reservaMiddleware import ReservaMiddleware
from api.controle.reservaControl import ReservaControl

class ReservaRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Reserva no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Reserva.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, Reserva_middleware: ReservaMiddleware, Reserva_control: ReservaControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param Reserva_middleware: Middleware com validações específicas para Reserva (ex.: validação de corpo, id).
        :param Reserva_control: Controlador que implementa a lógica de negócio (store, index, update, delete, show).

        Observações:
        - Blueprint é criado para permitir o registro isolado de rotas.
        - Injeção de dependência garante desacoplamento: o roteador não precisa criar middlewares ou controlador.
        """
        print("⬆️  ReservaRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__Reserva_middleware = Reserva_middleware
        self.__Reserva_control = Reserva_control

        # Blueprint é a coleção de rotas da entidade Reserva
        self.__blueprint = Blueprint('Reserva', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Reserva.

        Rotas implementadas:
        - POST /        -> Cria um novo Reserva
        - GET /         -> Lista todos os Reservas
        - GET /<id>     -> Retorna um Reserva por ID
        - PUT /<id>     -> Atualiza um Reserva por ID
        - DELETE /<id>  -> Remove um Reserva por ID

        Observações:
        - Cada rota aplica autenticação JWT.
        - Middlewares de validação são aplicados diretamente.
        - Para rotas que precisam do idReserva, o parâmetro vem da URI.
        """

        # POST / -> cria um Reserva
        @self.__blueprint.route('/', methods=['POST'])
        #@self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__Reserva_middleware.validate_body  # valida corpo da requisição
        def store():
            """
            Rota responsável por criar um novo Reserva.
            O corpo da requisição deve conter os dados do Reserva validados pelo middleware.
            """
            return self.__Reserva_control.store()

        # GET / -> lista todos os Reservas
        @self.__blueprint.route('/', methods=['GET'])
        @self.__jwt_middleware.validate_token  # valida token JWT

        def index():
            """
            Rota responsável por listar todos os Reservas cadastrados no sistema.
            """
            return self.__Reserva_control.index()

        # GET /<idReserva> -> retorna um Reserva específico
        @self.__blueprint.route('/<int:idReserva>', methods=['GET'])
        @self.__jwt_middleware.validate_token
        @self.__Reserva_middleware.validate_id_param  # valida se o ID é válido
        def show(idReserva):
            """
            Rota que retorna um Reserva específico pelo seu ID.

            :param idReserva: int - ID do Reserva vindo da URI.
            """
            return self.__Reserva_control.show()

        # PUT /<idReserva> -> atualiza um Reserva
        @self.__blueprint.route('/<int:idReserva>', methods=['PUT'])
        @self.__jwt_middleware.validate_token
        @self.__Reserva_middleware.validate_id_param
        @self.__Reserva_middleware.validate_body

        def update(idReserva):
            """
            Rota que atualiza um Reserva existente.

            Observações:
            - idReserva vem da URI (request.view_args['idReserva']).
            - Corpo da requisição validado pelo middleware validate_body.
            """
            return self.__Reserva_control.update()

        # DELETE /<idReserva> -> remove um Reserva
        @self.__blueprint.route('/<int:idReserva>', methods=['DELETE'])
        @self.__jwt_middleware.validate_token
        @self.__Reserva_middleware.validate_id_param
        
        def destroy(idReserva):
            """
            Rota que remove um Reserva pelo seu ID.

            :param idReserva: int - ID do Reserva a ser removido.
            """
            return self.__Reserva_control.destroy()

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint