# -*- coding: utf-8 -*-
from api.dao.hotelDAO import HotelDAO
from api.modelo.hotel import Hotel
from api.utils.errorResponse import ErrorResponse

"""
Classe responsável pela camada de serviço para a entidade Hotel.

Observações sobre injeção de dependência:
- O HotelService recebe uma instância de HotelDAO via construtor.
- Isso segue o padrão de injeção de dependência, tornando o serviço desacoplado
  do DAO concreto, facilitando testes unitários e substituição por mocks.
"""
class HotelService:
    def __init__(self, Hotel_dao_dependency: HotelDAO):
        """
        Construtor da classe HotelService

        :param Hotel_dao_dependency: HotelDAO - Instância de HotelDAO
        """
        print("⬆️  HotelService.__init__()")
        self.__HotelDAO = Hotel_dao_dependency  # injeção de dependência

    def createHotel(self, HotelBodyRequest: dict) -> int:
        """
        Cria um novo Hotel.

        :param HotelBodyRequest: dict - Dados do Hotel {"nomeHotel"}
        :return: int - ID do novo Hotel criado

        🔹 Validações:
        - nomeHotel não pode estar vazio
        - Não pode existir outro Hotel com mesmo nome
        """
        print("🟣 HotelService.createHotel()")

        hotel = Hotel()
        hotel.nome = HotelBodyRequest.get("nome")
        hotel.capacidade = HotelBodyRequest.get("capacidade")


        # valida regra de negócio: Hotel duplicado
        resultado = self.__HotelDAO.findByField("nome", hotel.nome)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Hotel já existe",
                {"message": f"O Hotel {hotel.nome} já existe"}
            )

        return self.__HotelDAO.create(hotel)

    def findAll(self) -> list[dict]:
        """
        Retorna todos os Hoteis
        :return: list[dict]
        """
        print("🟣 HotelService.findAll()")
        return self.__HotelDAO.findAll()

    def findById(self, idHotel: int) -> dict | None:
        """
        Retorna um Hotel por ID.

        :param idHotel: int
        :return: dict | None
        """
        print("🟣 HotelService.findById()")

        hotel = Hotel()
        hotel.idHotel = idHotel  # passa pela validação de domínio

        return self.__HotelDAO.findById(hotel.idHotel)

    def updateHotel(self, idHotel: int, jsonHotel: dict) -> bool:
        print (jsonHotel)
        """
        Atualiza um Hotel existente.

        🔹 Regra de domínio: o idHotel deve ser um número inteiro positivo.

        :param idHotel: int - Identificador do Hotel a ser atualizado
        :param jsonHotel: dict - Dados do Hotel {"nomeHotel", "email", "telefone", "requisicao", "cpf"}
        :return: bool - True se atualizado com sucesso
        :raises ValueError: se idHotel ou nomeHotel não atenderem às regras de domínio
        """
        print("🟣 HotelService.updateHotel()")

        hotel = Hotel()
        hotel.idHotel = idHotel
        hotel.nome = jsonHotel.get("nome")
        hotel.capacidade = jsonHotel.get("capacidade")

        return self.__HotelDAO.update(hotel)

    def deleteHotel(self, idHotel: int) -> bool:
        """
        Deleta um Hotel por ID.

        :param idHotel: int
        :return: bool
        """
        print("🟣 HotelService.deleteHotel()")

        hotel = Hotel()
        hotel.idHotel = idHotel  # validação de regra de domínio

        return self.__HotelDAO.delete(hotel)