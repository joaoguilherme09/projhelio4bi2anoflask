# -*- coding: utf-8 -*-
from flask import request, jsonify, g
from functools import wraps
from api.http.meu_token_jwt import MeuTokenJWT

class JwtMiddleware:
    """Middleware Flask para validação de tokens JWT"""

    def validate_token(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("🔷 JwtMiddleware.validate_token()")
            
            authorization = request.headers.get("Authorization", None)
            jwt_instance = MeuTokenJWT()

            if jwt_instance.validar_token(authorization):
                # ✅ Armazena payload no contexto Flask
                g.jwt_payload = jwt_instance.payload
                return f(*args, **kwargs)
            else:
                return jsonify({
                    "success": False,
                    "error": {
                        "message": jwt_instance.error_message or "Token inválido",
                        "code": "INVALID_TOKEN"
                    }
                }), 401

        return decorated_function
