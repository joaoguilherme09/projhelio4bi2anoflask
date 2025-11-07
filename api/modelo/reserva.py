from api.modelo.hospede import Hospede
from api.modelo.hotel import Hotel
from datetime import datetime, date

class Reserva:
    def __init__(self):
        self.__idReserva = None
        self.__idHospede = None
        self.__idHotel = None
        self.__inicio = None
        self.__fim = None

    @property
    def idReserva(self):
        return self.__idReserva

    @idReserva.setter
    def idReserva(self, value):
        try:
            id_val = int(value)
        except (ValueError, TypeError):
            raise ValueError("idReserva deve ser um número inteiro.")

        if id_val <= 0:
            raise ValueError("idReserva deve ser um número inteiro positivo.")

        self.__idReserva = id_val

    @property
    def idHospede(self):
        return self.__idHospede

    @idHospede.setter
    def idHospede(self, value):
        try:
            id_val = int(value)
        except (ValueError, TypeError):
            raise ValueError("idHospede deve ser um número inteiro.")

        if id_val <= 0:
            raise ValueError("idHospede deve ser um número inteiro positivo.")

        self.__idHospede = id_val

    @property
    def idHotel(self):
        return self.__idHotel

    @idHotel.setter
    def idHotel(self, value):
        try:
            id_val = int(value)
        except (ValueError, TypeError):
            raise ValueError("idHotel deve ser um número inteiro.")

        if id_val <= 0:
            raise ValueError("idHotel deve ser um número inteiro positivo.")

        self.__idHotel = id_val

    @property
    def inicio(self):
        return self.__inicio

    @inicio.setter
    def inicio(self, valor):
        """
        🔹 REGRA DE DOMÍNIO: Data de início da reserva
        
        Validações:
        1. Deve ser uma data válida (string no formato YYYY-MM-DD ou objeto date)
        2. Não pode ser uma data no passado (data mínima é hoje)
        3. Deve ser anterior à data de fim (se ambas estiverem definidas)
        """
        data_inicio = self.__converter_para_date(valor)
        
        # Verifica se é uma data válida
        if not data_inicio:
            raise ValueError("Data de início deve ser uma data válida no formato YYYY-MM-DD")
        
        # Data não pode ser no passado
        hoje = date.today()
        if data_inicio < hoje:
            raise ValueError("Data de início não pode ser no passado")
        
        # Se já tiver data de fim definida, verifica se início é anterior ao fim
        if self.__fim and data_inicio >= self.__fim:
            raise ValueError("Data de início deve ser anterior à data de fim")
        
        self.__inicio = data_inicio

    @property
    def fim(self):
        return self.__fim

    @fim.setter
    def fim(self, valor):
        """
        🔹 REGRA DE DOMÍNIO: Data de fim da reserva
        
        Validações:
        1. Deve ser uma data válida (string no formato YYYY-MM-DD ou objeto date)
        2. Deve ser posterior à data de início (se ambas estiverem definidas)
        3. Período mínimo de 1 dia de reserva
        """
        data_fim = self.__converter_para_date(valor)
        
        # Verifica se é uma data válida
        if not data_fim:
            raise ValueError("Data de fim deve ser uma data válida no formato YYYY-MM-DD")
        
        # Se já tiver data de início definida, verifica se fim é posterior ao início
        if self.__inicio:
            if data_fim <= self.__inicio:
                raise ValueError("Data de fim deve ser posterior à data de início")
            
            # Verifica período mínimo de 1 dia
            if (data_fim - self.__inicio).days < 1:
                raise ValueError("Período de reserva deve ser de pelo menos 1 dia")
        
        self.__fim = data_fim

    def __converter_para_date(self, valor):
        """
        Método auxiliar para converter string para date
        
        Aceita:
        - Objeto date (retorna diretamente)
        - String no formato YYYY-MM-DD
        - String no formato DD/MM/YYYY
        """
        if isinstance(valor, date):
            return valor
        
        if not isinstance(valor, str):
            return None
        
        # Tenta formato YYYY-MM-DD (padrão ISO/banco de dados)
        try:
            return datetime.strptime(valor, '%Y-%m-%d').date()
        except ValueError:
            pass
        
        # Tenta formato DD/MM/YYYY (comum no Brasil)
        try:
            return datetime.strptime(valor, '%d/%m/%Y').date()
        except ValueError:
            pass
        
        return None

    def validar_periodo_reserva(self):
        """
        🔹 REGRA DE DOMÍNIO: Validação completa do período da reserva
        
        Esta validação deve ser chamada após definir ambas as datas
        para garantir a consistência do domínio.
        """
        if not self.__inicio or not self.__fim:
            raise ValueError("Ambas as datas (início e fim) devem ser definidas")
        
        if self.__inicio >= self.__fim:
            raise ValueError("Data de início deve ser anterior à data de fim")
        
        periodo_dias = (self.__fim - self.__inicio).days
        if periodo_dias < 1:
            raise ValueError("Período de reserva deve ser de pelo menos 1 dia")
        
        if periodo_dias > 365:  # Máximo de 1 ano de reserva
            raise ValueError("Período de reserva não pode exceder 1 ano")
        
        return True

