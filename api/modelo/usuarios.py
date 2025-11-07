import re

class Usuario:
    def init(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        # Atributos privados de instância
        self.__idUsuario = None
        self.__nome = None
        self.__email = None
        self.__senha = None
        self.__role = None
        self.__ativo = True

    @property
    def idUsuario(self):
        return self.__idUsuario

    @idUsuario.setter
    def idUsuario(self, value):
        try:
            id_val = int(value)
        except (ValueError, TypeError):
            raise ValueError("idUsuario deve ser um número inteiro.")
        
        if id_val <= 0:
            raise ValueError("idUsuario deve ser positivo.")
        
        self.__idUsuario = id_val

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, value):
        if not isinstance(value, str):
            raise ValueError("nome deve ser uma string.")
        
        nome = value.strip()
        if len(nome) < 3:
            raise ValueError("nome deve ter pelo menos 3 caracteres.")
        
        self.__nome = nome

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise ValueError("email deve ser uma string.")
        
        email = value.strip()
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
            raise ValueError("email inválido.")
        
        self.__email = email

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, value):
        if not isinstance(value, str):
            raise ValueError("senha deve ser uma string.")
        
        if len(value) < 6:
            raise ValueError("senha deve ter pelo menos 6 caracteres.")
        
        self.__senha = value

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, value):
        roles_validas = ['admin', 'funcionario', 'gerente']
        if value not in roles_validas:
            raise ValueError(f"role deve ser uma das seguintes: {', '.join(roles_validas)}")
        
        self.__role = value

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, value):
        self.__ativo = bool(value)

    

