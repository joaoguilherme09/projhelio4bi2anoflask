# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from api.utils.errorResponse import ErrorResponse

class HotelMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Hotel.

    Objetivos:
    - Garantir que os dados obrigatórios estejam presentes antes de chamar
      os métodos do Controller ou Service.
    - Lançar erros padronizados usando ErrorResponse quando a validação falhar.
    """

    def validate_body(self, f):
        """
        Decorator para validar o corpo da requisição (JSON) para operações de Hotel.

        Verifica apenas a existência:
        - O objeto 'Hotel' existe
        - O campo obrigatório 'nomeHotel' está presente
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 HotelMiddleware.validate_body()")
            body = request.get_json()

            if not body or 'Hotel' not in body:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'Hotel' é obrigatório!"}
                )

            Hotel = body['Hotel']
            if 'nome' not in Hotel:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O campo 'nome' é obrigatório!"}
                )

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """
        Decorator para validar o parâmetro de rota 'idHotel'.

        Verifica apenas a existência do parâmetro.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 HotelMiddleware.validate_id_param()")
            if 'idHotel' not in kwargs:
                raise ErrorResponse(
                    400, "Erro na validação de dados",
                    {"message": "O parâmetro 'idHotel' é obrigatório!"}
                )
            return f(*args, **kwargs)
        return decorated_function