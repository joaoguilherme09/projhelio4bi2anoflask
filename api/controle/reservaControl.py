from flask import request, jsonify
from api.service.reservaService import ReservaService
"""
Classe responsável por controlar os endpoints da API REST para a entidade Reserva.

Esta classe implementa métodos CRUD e utiliza injeção de dependência
para receber a instância de ReservaService, desacoplando a lógica de negócio
da camada de controle.
"""
class ReservaControl:
    def __init__(self, Reserva_service:ReservaService):
        """
        Construtor da classe ReservaControl
        :param Reserva_service: Instância do ReservaService (injeção de dependência)
        """
        print("⬆️  ReservaControl.constructor()")
        self.__Reserva_service = Reserva_service

    def store(self):
        """Cria um novo Reserva"""
        print("🔵 ReservaControle.store()")
       
        Reserva_body_request = request.json.get("Reserva")  #Pega os dados do Reserva no corpo da requisição
        novo_id = self.__Reserva_service.createReserva(Reserva_body_request)

        obj_resposta = {
            "success": True,
            "message": "Cadastro realizado com sucesso",
            "data": {
                "reservas": [  # ✅ CORREÇÃO: Minúsculo para padronizar
                    {
                        "idReserva": novo_id,
                        "idHospede": Reserva_body_request.get("idHospede"),
                        "idHotel": Reserva_body_request.get("idHotel"),
                        "inicio": Reserva_body_request.get("inicio"),
                        "fim": Reserva_body_request.get("fim")
                    }
                ]
            }
        }

        if novo_id:
            return jsonify(obj_resposta), 200
        

    def index(self):
        """Lista todos os Reservas cadastrados"""
        print("🔵 ReservaControle.index()")
       
        array_Reservas = self.__Reserva_service.findAll()
        
        return jsonify({
            "success": True,
            "message": "Busca realizada com sucesso",
            "data": {"reservas": array_Reservas}  # ✅ CORREÇÃO: Minúsculo para padronizar
        }), 200
        

    def show(self):
          # Pega o idReserva diretamente da URI
        idReserva = request.view_args.get("idReserva")

        Reserva = self.__Reserva_service.findById(idReserva)
        
        # ✅ CORREÇÃO: Validar se reserva existe antes de retornar
        if not Reserva:
            return jsonify({
                "success": False,
                "message": f"Reserva com ID {idReserva} não encontrada",
                "data": None
            }), 404
        
        obj_resposta = {
            "success": True,
            "message": "Executado com sucesso",
            "data": {"reserva": Reserva}  # ✅ CORREÇÃO: Singular para um único item
        }
        return jsonify(obj_resposta), 200
      

    def update(self):
        """Atualiza os dados de um Reserva existente"""
        print("🔵 ReservaControle.update()")
       
        # Pega o idReserva diretamente da URI
        idReserva = request.view_args.get("idReserva")

        # Pega os dados do Reserva no corpo da requisição
        json_Reserva = request.json.get("Reserva")
        print(f"📦 CONTROLLER UPDATE - ID: {idReserva}, Dados: {json_Reserva}")

        resposta = self.__Reserva_service.updateReserva(idReserva, json_Reserva)
        
        # ✅ CORREÇÃO: Validar se a atualização foi bem-sucedida
        if not resposta:
            return jsonify({
                "success": False,
                "message": f"Falha ao atualizar reserva ID {idReserva}",
                "data": None
            }), 400
        
        return jsonify({
            "success": True,
            "message": "Reserva atualizada com sucesso",
            "data": {
                "reserva": {  # ✅ CORREÇÃO: Singular para consistência
                    "idReserva": int(idReserva),
                    "idHospede": json_Reserva.get("idHospede"),
                    "idHotel": json_Reserva.get("idHotel"),
                    "inicio": json_Reserva.get("inicio"),
                    "fim": json_Reserva.get("fim")
                }
            }
        }), 200
   

    def destroy(self):
        """Remove um Reserva pelo ID"""
        print("🔵 ReservaControle.destroy()")
        # Pega o idReserva diretamente da URI
        idReserva = request.view_args.get("idReserva")
        
        excluiu = self.__Reserva_service.deleteReserva(idReserva)
        if not excluiu:
            return jsonify({
                "success": False,
                "message": f"Não existe Reserva com id {idReserva}"
            }), 404

        return jsonify({
            "success": True,
            "message": "Excluído com sucesso"
        }), 200