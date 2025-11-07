# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.errorResponse import ErrorResponse

class HospedeMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Hospede.

    Objetivos:
    - Garantir que os dados obrigatórios estejam presentes antes de chamar
      os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição (JSON) para operações de Hospede.

        Verifica apenas a existência:
        - O objeto 'Hospede' existe
        - O campo obrigatório 'nomeHospede' está presente
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 HospedeMiddleware.validate_body()")
            body = request.get_json()

            if not body or 'Hospede' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'Hospede' é obrigatório!"}
                )

            Hospede = body['Hospede']
            if 'nomeHospede' not in Hospede:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nomeHospede' é obrigatório!"}
                )

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'idHospede'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 HospedeMiddleware.validate_id_param()")
            if 'idHospede' not in kwargs:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'idHospede' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function