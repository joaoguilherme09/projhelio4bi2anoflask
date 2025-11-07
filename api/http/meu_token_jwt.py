# -*- coding: utf-8 -*-
import jwt
import time
import secrets

class MeuTokenJWT:
    """Classe para gerar e validar tokens JWT"""
    
    def __init__(self):
        # ⚠️ IMPORTANTE: Mova para variável de ambiente em produção!
        self._key = "x9S4q0v+V0IjvHkG20uAxaHx1ijj+q1HWjHKv+ohxp/oK+77qyXkVj/l4QYHHTF3"
        self._alg = "HS256"
        self._iss = "http://localhost"
        self._aud = "http://localhost"
        self._sub = "acesso_sistema"
        self._duracao_token = 3600  # 1 hora (recomendado ao invés de 60 dias!)
        self._payload = None
        self._error_message = None

    @property
    def payload(self):
        return self._payload
    
    @property
    def error_message(self):
        return self._error_message

    def gerar_token(self, claims: dict) -> str:
        """
        Gera um token JWT com os claims fornecidos
        
        :param claims: dict - Dados do usuário (user_id, email, role, etc)
        :return: str - Token JWT
        """
        payload = {
            "iss": self._iss,
            "aud": self._aud,
            "sub": self._sub,
            "iat": int(time.time()),
            "exp": int(time.time()) + self._duracao_token,
            "nbf": int(time.time()),
            "jti": secrets.token_hex(16),
            **claims  # Adiciona os claims personalizados
        }
        token = jwt.encode(payload, self._key, algorithm=self._alg)
        return token

    def validar_token(self, token: str) -> bool:
        """
        Valida um token JWT
        
        :param token: str - Token JWT (pode incluir "Bearer ")
        :return: bool - True se válido, False caso contrário
        """
        if not token:
            print("❌ Token não fornecido")
            self._error_message = "Token não fornecido"
            return False

        # Remove "Bearer " se presente
        token = token.replace("Bearer ", "").strip()

        try:
            decoded = jwt.decode(
                token, 
                self._key, 
                algorithms=[self._alg], 
                audience=self._aud, 
                issuer=self._iss
            )
            self._payload = decoded
            self._error_message = None
            print("✅ Token válido")
            return True
        except jwt.ExpiredSignatureError:
            print("❌ Token expirado")
            self._error_message = "Token expirado"
        except jwt.InvalidAudienceError:
            print("❌ Audiência inválida")
            self._error_message = "Token inválido - audiência incorreta"
        except jwt.InvalidIssuerError:
            print("❌ Emissor inválido")
            self._error_message = "Token inválido - emissor incorreto"
        except jwt.InvalidTokenError as e:
            print(f"❌ Token inválido: {str(e)}")
            self._error_message = "Token inválido"
        except Exception as e:
            print(f"❌ Erro ao validar token: {str(e)}")
            self._error_message = "Erro ao validar token"
        
        return False