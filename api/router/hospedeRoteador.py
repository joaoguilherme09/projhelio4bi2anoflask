# -*- coding: utf-8 -*-
from flask import Blueprint, request
from api.Middleware.jwt_middleware import JwtMiddleware
from api.Middleware.hospedeMiddleware import HospedeMiddleware
from api.controle.hospedeControl import HospedeControl

class HospedeRoteador:
    """
    Classe responsável por configurar todas as rotas da entidade Hospede no Flask.

    Objetivos:
    - Criar um Blueprint isolado para as rotas de Hospede.
    - Receber middlewares e controlador via injeção de dependência.
    - Aplicar autenticação JWT e validações antes de chamar o controlador.
    """

    def __init__(self, jwt_middleware: JwtMiddleware, Hospede_middleware: HospedeMiddleware, Hospede_control: HospedeControl):
        """
        Construtor do roteador.

        :param jwt_middleware: Middleware responsável por validar token JWT.
        :param Hospede_middleware: Middleware com validações específicas para Hospede (ex.: validação de corpo, id).
        :param Hospede_control: Controlador que implementa a lógica de negócio (store, index, update, delete, show).

        Observações:
        - Blueprint é criado para permitir o registro isolado de rotas.
        - Injeção de dependência garante desacoplamento: o roteador não precisa criar middlewares ou controlador.
        """
        print("⬆️ HospedeRoteador.__init__()")
        self.__jwt_middleware = jwt_middleware
        self.__Hospede_middleware = Hospede_middleware
        self.__Hospede_control = Hospede_control

        # Blueprint é a coleção de rotas da entidade Hospede
        self.__blueprint = Blueprint('Hospede', __name__)

    def create_routes(self):
        """
        Configura e retorna todas as rotas REST da entidade Hospede.

        Rotas implementadas:
        - POST /        -> Cria um novo Hospede
        - GET /         -> Lista todos os Hospedes
        - GET /<id>     -> Retorna um Hospede por ID
        - PUT /<id>     -> Atualiza um Hospede por ID
        - DELETE /<id>  -> Remove um Hospede por ID

        Observações:
        - Cada rota aplica autenticação JWT.
        - Middlewares de validação são aplicados diretamente.
        - Para rotas que precisam do idHospede, o parâmetro vem da URI.
        """

        # POST / -> cria um Hospede
        @self.__blueprint.route('/', methods=['POST'], strict_slashes=False)
        @self.__jwt_middleware.validate_token  # valida token JWT antes de executar
        @self.__Hospede_middleware.validate_body  # valida corpo da requisição
        def store():
            """
            Rota responsável por criar um novo Hospede.
            O corpo da requisição deve conter os dados do Hospede validados pelo middleware.
            """
            return self.__Hospede_control.store()

        # GET / -> lista todos os Hospedes
        @self.__blueprint.route('/', methods=['GET'], strict_slashes=False)
        @self.__jwt_middleware.validate_token  # valida token JWT
        def index():
            """
            Rota responsável por listar todos os Hospedes cadastrados no sistema.
            """
            return self.__Hospede_control.index()

        # GET /<idHospede> -> retorna um Hospede específico
        @self.__blueprint.route('/<int:idHospede>', methods=['GET'], strict_slashes=False)
        @self.__jwt_middleware.validate_token
        @self.__Hospede_middleware.validate_id_param  # valida se o ID é válido
        def show(idHospede):
            """
            Rota que retorna um Hospede específico pelo seu ID.

            :param idHospede: int - ID do Hospede vindo da URI.
            """
            return self.__Hospede_control.show()

        # PUT /<idHospede> -> atualiza um Hospede
        @self.__blueprint.route('/<int:idHospede>', methods=['PUT'], strict_slashes=False)
        @self.__jwt_middleware.validate_token
        @self.__Hospede_middleware.validate_id_param
        @self.__Hospede_middleware.validate_body
        def update(idHospede):
            """
            Rota que atualiza um Hospede existente.

            Observações:
            - idHospede vem da URI (request.view_args['idHospede']).
            - Corpo da requisição validado pelo middleware validate_body.
            """
            return self.__Hospede_control.update()

        # DELETE /<idHospede> -> remove um Hospede
        @self.__blueprint.route('/<int:idHospede>', methods=['DELETE'], strict_slashes=False)
        @self.__jwt_middleware.validate_token
        @self.__Hospede_middleware.validate_id_param
        def destroy(idHospede):
            """
            Rota que remove um Hospede pelo seu ID.

            :param idHospede: int - ID do Hospede a ser removido.
            """
            return self.__Hospede_control.destroy()

        # Retorna o Blueprint configurado para registro na aplicação Flask
        return self.__blueprint