from flask import request, jsonify
from api.service.hotelService import HotelService
"""
Classe responsável por controlar os endpoints da API REST para a entidade Hotel.

Esta classe implementa métodos CRUD e utiliza injeção de dependência
para receber a instância de HotelService, desacoplando a lógica de negócio
da camada de controle.
"""
class HotelControl:
    def __init__(self, Hotel_service:HotelService):
        """
        Construtor da classe HotelControl
        :param Hotel_service: Instância do HotelService (injeção de dependência)
        """
        print("⬆️  HotelControl.constructor()")
        self.__Hotel_service = Hotel_service

    def store(self):
        """Cria um novo Hotel"""
        print("🔵 HotelControle.store()")
       
        Hotel_body_request = request.json.get("Hotel")  #Pega os dados do Hotel no corpo da requisição
        novo_id = self.__Hotel_service.createHotel(Hotel_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "Hoteis": [
                    {
                        "idHotel": novo_id,
                        "nomeHotel": Hotel_body_request.get("nome"),
                        "capacidade": Hotel_body_request.get("capacidade"),
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        """Lista todos os Hoteis cadastrados"""
        print("🔵 HotelControle.index()")
       
        array_Hoteis = self.__Hotel_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"Hoteis": array_Hoteis}
        }), 200
        

    def show(self):
          # Pega o idHotel diretamente da URI
        idHotel = request.view_args.get("idHotel")

        Hotel = self.__Hotel_service.findById(idHotel)
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"Hoteis": Hotel}
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        """Atualiza os dados de um Hotel existente"""
        print("🔵 HotelControle.update()")
       
        # Pega o idHotel diretamente da URI
        idHotel = request.view_args.get("idHotel")

        # Pega os dados do Hotel no corpo da requisição
        json_Hotel = request.json.get("Hotel")
        print(json_Hotel)

        resposta = self.__Hotel_service.updateHotel(idHotel, json_Hotel)
        return jsonify({
            "success": True,
            "message": "Hotel atualizado com sucesso",
            "data": {
                "Hotel": {
                    "idHotel": int(idHotel),
                    "nomeHotel": json_Hotel.get("nome"),
                    "capacidade": json_Hotel.get("capacidade")
                }
            }
        }), 200
   

    def destroy(self):
        """Remove um Hotel pelo ID"""
        print("🔵 HotelControle.destroy()")
        # Pega o idHotel diretamente da URI
        idHotel = request.view_args.get("idHotel")
        
        excluiu = self.__Hotel_service.deleteHotel(idHotel)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe Hotel com id {idHotel}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 200
        