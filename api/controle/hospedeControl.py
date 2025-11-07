from flask import request, jsonify
from api.service.hospedeService import HospedeService
"""
Classe responsável por controlar os endpoints da API REST para a entidade Hospede.

Esta classe implementa métodos CRUD e utiliza injeção de dependência
para receber a instância de HospedeService, desacoplando a lógica de negócio
da camada de controle.
"""
class HospedeControl:
    def __init__(self, Hospede_service:HospedeService):
        """
        Construtor da classe HospedeControl
        :param Hospede_service: Instância do HospedeService (injeção de dependência)
        """
        print("⬆️  HospedeControl.constructor()")
        self.__Hospede_service = Hospede_service

    def store(self):
        """Cria um novo Hospede"""
        print("🔵 HospedeControle.store()")
       
        Hospede_body_request = request.json.get("Hospede")  #Pega os dados do Hospede no corpo da requisição
        novo_id = self.__Hospede_service.createHospede(Hospede_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "Hospedes": [
                    {
                        "idHospede": novo_id,
                        "nomeHospede": Hospede_body_request.get("nomeHospede"),
                        "email": Hospede_body_request.get("email"),
                        "telefone": Hospede_body_request.get("telefone"),
                        "requisicao": Hospede_body_request.get("requisicao"),
                        "cpf": Hospede_body_request.get("cpf")
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        """Lista todos os Hospedes cadastrados"""
        print("🔵 HospedeControle.index()")
       
        array_Hospedes = self.__Hospede_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"Hospedes": array_Hospedes}
        }), 200
        

    def show(self):
          # Pega o idHospede diretamente da URI
        idHospede = request.view_args.get("idHospede")

        Hospede = self.__Hospede_service.findById(idHospede)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"Hospedes": Hospede}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        """Atualiza os dados de um Hospede existente"""
        print("🔵 HospedeControle.update()")
       
        # Pega o idHospede diretamente da URI
        idHospede = request.view_args.get("idHospede")

        # Pega os dados do Hospede no corpo da requisição
        json_Hospede = request.json.get("Hospede")
        print(json_Hospede)

        resposta = self.__Hospede_service.updateHospede(idHospede, json_Hospede)
        return jsonify({
            "success": True,
            "message": "Hospede atualizado com sucesso",
            "data": {
                "Hospede": {
                    "idHospede": int(idHospede),
                    "nomeHospede": json_Hospede.get("nomeHospede")
                }
            }
        }), 200
   

    def destroy(self):
        """Remove um Hospede pelo ID"""
        print("🔵 HospedeControle.destroy()")
        # Pega o idHospede diretamente da URI
        idHospede = request.view_args.get("idHospede")
        
        excluiu = self.__Hospede_service.deleteHospede(idHospede)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe Hospede com id {idHospede}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 200
        