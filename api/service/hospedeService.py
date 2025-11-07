# -*- coding: utf-8 -*-
from api.dao.hospedeDAO import HospedeDAO
from api.modelo.hospede import Hospede
from api.utils.errorResponse import ErrorResponse

"""
Classe responsável pela camada de serviço para a entidade Hospede.

Observações sobre injeção de dependência:
- O HospedeService recebe uma instância de HospedeDAO via construtor.
- Isso segue o padrão de injeção de dependência, tornando o serviço desacoplado
  do DAO concreto, facilitando testes unitários e substituição por mocks.
"""
class HospedeService:
    def __init__(self, Hospede_dao_dependency: HospedeDAO):
        """
        Construtor da classe HospedeService

        :param Hospede_dao_dependency: HospedeDAO - Instância de HospedeDAO
        """
        print("⬆️  HospedeService.__init__()")
        self.__HospedeDAO = Hospede_dao_dependency  # injeção de dependência

    def createHospede(self, HospedeBodyRequest: dict) -> int:
        """
        Cria um novo Hospede.

        :param HospedeBodyRequest: dict - Dados do Hospede {"nomeHospede"}
        :return: int - ID do novo Hospede criado

        🔹 Validações:
        - nomeHospede não pode estar vazio
        - Não pode existir outro Hospede com mesmo nome
        """
        print("🟣 HospedeService.createHospede()")

        hospede = Hospede()
        hospede.nomeHospede = HospedeBodyRequest.get("nomeHospede")
        hospede.email = HospedeBodyRequest.get("email")
        hospede.telefone = HospedeBodyRequest.get("telefone")
        hospede.requisicao = HospedeBodyRequest.get("requisicao")
        hospede.cpf = HospedeBodyRequest.get("cpf")

        # valida regra de negócio: Hospede duplicado
        resultado = self.__HospedeDAO.findByField("nome", hospede.nomeHospede)
        if resultado and len(resultado) > 0:
            raise ErrorResponse(
                400,
                "Hospede já existe",
                {"message": f"O Hospede {hospede.nomeHospede} já existe"}
            )

        return self.__HospedeDAO.create(hospede)

    def findAll(self) -> list[dict]:
        """
        Retorna todos os Hospedes
        :return: list[dict]
        """
        print("🟣 HospedeService.findAll()")
        return self.__HospedeDAO.findAll()

    def findById(self, idHospede: int) -> dict | None:
        """
        Retorna um Hospede por ID.

        :param idHospede: int
        :return: dict | None
        """
        print("🟣 HospedeService.findById()")

        hospede = Hospede()
        hospede.idHospede = idHospede  # passa pela validação de domínio

        return self.__HospedeDAO.findById(hospede.idHospede)

    def updateHospede(self, idHospede: int, jsonHospede: dict) -> bool:
        print (jsonHospede)
        """
        Atualiza um Hospede existente.

        🔹 Regra de domínio: o idHospede deve ser um número inteiro positivo.

        :param idHospede: int - Identificador do Hospede a ser atualizado
        :param jsonHospede: dict - Dados do Hospede {"nomeHospede", "email", "telefone", "requisicao", "cpf"}
        :return: bool - True se atualizado com sucesso
        :raises ValueError: se idHospede ou nomeHospede não atenderem às regras de domínio
        """
        print("🟣 HospedeService.updateHospede()")

        hospede = Hospede()
        hospede.idHospede = idHospede
        hospede.nomeHospede = jsonHospede.get("nomeHospede")
        hospede.email = jsonHospede.get("email")
        hospede.telefone = jsonHospede.get("telefone")
        hospede.requisicao = jsonHospede.get("requisicao")
        hospede.cpf = jsonHospede.get("cpf")

        return self.__HospedeDAO.update(hospede)

    def deleteHospede(self, idHospede: int) -> bool:
        """
        Deleta um Hospede por ID.

        :param idHospede: int
        :return: bool
        """
        print("🟣 HospedeService.deleteHospede()")

        hospede = Hospede()
        hospede.idHospede = idHospede  # validação de regra de domínio

        return self.__HospedeDAO.delete(hospede)