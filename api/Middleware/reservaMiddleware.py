# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from datetime import datetime, date
from api.utils.errorResponse import ErrorResponse


class ReservaMiddleware:
    """
    Middleware para validação de requisições relacionadas à entidade Reserva.

    Validações incluídas:
    - Corpo da requisição (existência de 'Reserva' e campos obrigatórios)
    - Formato das datas (YYYY-MM-DD)
    - Ordem cronológica (inicio < fim)
    - Data de início não anterior a hoje
    - idHospede / idHotel devem ser inteiros positivos
    """

    def validate_body(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ReservaMiddleware.validate_body()")
            body = request.get_json()
            errors = []

            if not body or 'Reserva' not in body:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O campo 'Reserva' é obrigatório!"})

            reserva = body['Reserva']

            # campos obrigatórios
            required = ['idHospede', 'idHotel', 'inicio', 'fim']
            for campo in required:
                if campo not in reserva:
                    errors.append(f"O campo '{campo}' é obrigatório.")

            # validar ids
            if 'idHospede' in reserva:
                try:
                    ii = int(reserva.get('idHospede'))
                    if ii <= 0:
                        errors.append("idHospede deve ser um inteiro positivo.")
                except (ValueError, TypeError):
                    errors.append("idHospede deve ser um inteiro.")

            if 'idHotel' in reserva:
                try:
                    ic = int(reserva.get('idHotel'))
                    if ic <= 0:
                        errors.append("idHotel deve ser um inteiro positivo.")
                except (ValueError, TypeError):
                    errors.append("idHotel deve ser um inteiro.")

            # validar datas
            di = None
            df = None
            if 'inicio' in reserva:
                try:
                    di = datetime.strptime(str(reserva.get('inicio')), "%Y-%m-%d").date()
                except Exception:
                    errors.append("Data de início inválida ou formato incorreto (esperado YYYY-MM-DD).")
            if 'fim' in reserva:
                try:
                    df = datetime.strptime(str(reserva.get('fim')), "%Y-%m-%d").date()
                except Exception:
                    errors.append("Data de fim inválida ou formato incorreto (esperado YYYY-MM-DD).")

            if di and df:
                if df <= di:
                    errors.append("Data de fim deve ser posterior à data de início.")
                if di < date.today():
                    errors.append("Data de início não pode ser anterior a hoje.")

            if errors:
                raise ErrorResponse(400, "Erro na validação de dados da Reserva", {"errors": errors})

            return f(*args, **kwargs)
        return decorated_function

    def validate_id_param(self, f):
        """Valida parâmetro de rota 'idReserva' (presença e inteiro positivo)."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 ReservaMiddleware.validate_id_param()")
            if 'idReserva' not in kwargs:
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "O parâmetro 'idReserva' é obrigatório!"})
            try:
                val = int(kwargs.get('idReserva'))
                if val <= 0:
                    raise ErrorResponse(400, "Erro na validação de dados", {"message": "idReserva deve ser um inteiro positivo."})
            except (ValueError, TypeError):
                raise ErrorResponse(400, "Erro na validação de dados", {"message": "idReserva deve ser um inteiro."})
            return f(*args, **kwargs)
        return decorated_function
