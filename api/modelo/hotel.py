class Hotel:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        # Atributos privados de instância
        self.__idHotel = None
        self.__nome = None
        self.__capacidade = None
    
    @property
    def idHotel(self):
        """
        Getter para idHotel
        :return: int - Identificador do hotel
        """
        return self.__idHotel
    @idHotel.setter
    def idHotel(self, valor):   
        try:
            parsed = int(valor)
        except (ValueError, TypeError):
            raise ValueError("idHospede deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("idHospede deve ser um número inteiro positivo.")

        self.__idHotel = parsed

    @property
    def nome(self):
        """
        Getter para nome
        :return: str - Nome do hotel
        """
        return self.__nome
    @nome.setter
    def nome(self, value):
        if not isinstance(value, str):
            raise ValueError("nomeHospede deve ser uma string.")

        nome = value.strip()

        if len(nome) < 3:
            raise ValueError("nomeHospede deve ter pelo menos 3 caracteres.")
        self.__nome = nome

    @property
    def capacidade(self):
        return self.__capacidade
    
    @capacidade.setter
    def capacidade(self, valor):
        try:
            capacidade = int(valor)
        except (ValueError, TypeError):
            raise ValueError("capacidade deve ser um número inteiro.")

        if capacidade <= 0:
            raise ValueError("capacidade deve ser um número inteiro positivo.")

        self.__capacidade = capacidade