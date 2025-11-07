# -*- coding: utf-8 -*-
from api.dao.reservaDAO import ReservaDAO
from api.dao.hospedeDAO import HospedeDAO
from api.dao.hotelDAO import HotelDAO
from api.modelo.reserva import Reserva
from api.utils.errorResponse import ErrorResponse
from datetime import datetime, date

class ReservaService:
	def __init__(self, reserva_dao: ReservaDAO, hospede_dao: HospedeDAO, hotel_dao: HotelDAO):
		print("⬆️  ReservaService.__init__()")
		self.__ReservaDAO = reserva_dao
		self.__HospedeDAO = hospede_dao
		self.__HotelDAO = hotel_dao

	def createReserva(self, reservaBodyRequest: dict) -> int:
		print("🟣 ReservaService.createReserva()")
		print(f"   📦 Dados recebidos: {reservaBodyRequest}")

		# Validação de campos obrigatórios
		idHospede = reservaBodyRequest.get("idHospede")
		idHotel = reservaBodyRequest.get("idHotel")
		inicio = reservaBodyRequest.get("inicio")
		fim = reservaBodyRequest.get("fim")

		# ✅ CORREÇÃO: Log detalhado dos dados recebidos
		print(f"   🔍 idHospede: {idHospede} (tipo: {type(idHospede)})")
		print(f"   🔍 idHotel: {idHotel} (tipo: {type(idHotel)})")
		print(f"   🔍 inicio: {inicio} (tipo: {type(inicio)})")
		print(f"   🔍 fim: {fim} (tipo: {type(fim)})")

		# Validação de chaves estrangeiras
		if not idHospede or not self.__HospedeDAO.findById(idHospede):
			raise ErrorResponse(400, "Hospede não encontrado", {"message": f"idHospede {idHospede} não existe"})
		if not idHotel or not self.__HotelDAO.findById(idHotel):
			raise ErrorResponse(400, "Hotel não encontrado", {"message": f"idHotel {idHotel} não existe"})

		# Validação de datas
		valid, errors = self._validar_datas(inicio, fim)
		if not valid:
			print(f"   ❌ Erros de validação de datas: {errors}")
			raise ErrorResponse(400, "Erro de validação de datas", {"errors": errors})

		# Impedir sobreposição de reservas para o mesmo hotel
		if self._existe_sobreposicao(idHotel, inicio, fim):
			raise ErrorResponse(400, "Conflito de reserva", {"message": "Já existe uma reserva para este hotel neste período."})

		reserva = Reserva()
		reserva.idHospede = idHospede
		reserva.idHotel = idHotel
		reserva.inicio = inicio
		reserva.fim = fim

		novo_id = self.__ReservaDAO.create(reserva)
		print(f"   ✅ Reserva criada com ID: {novo_id}")
		return novo_id

	def _validar_datas(self, inicio, fim):
		"""
		✅ CORREÇÃO: Validação robusta de datas com múltiplos formatos
		"""
		errors = []
		di = None
		df = None
		
		# Tentar converter data de início
		try:
			if isinstance(inicio, date):
				di = inicio
			elif isinstance(inicio, datetime):
				di = inicio.date()
			elif isinstance(inicio, str):
				# Tentar formato YYYY-MM-DD
				di = datetime.strptime(str(inicio), "%Y-%m-%d").date()
			else:
				errors.append(f"Formato de data de início inválido: {type(inicio)}")
		except Exception as e:
			errors.append(f"Data de início inválida ou formato incorreto (esperado YYYY-MM-DD). Erro: {str(e)}")
		
		# Tentar converter data de fim
		try:
			if isinstance(fim, date):
				df = fim
			elif isinstance(fim, datetime):
				df = fim.date()
			elif isinstance(fim, str):
				# Tentar formato YYYY-MM-DD
				df = datetime.strptime(str(fim), "%Y-%m-%d").date()
			else:
				errors.append(f"Formato de data de fim inválido: {type(fim)}")
		except Exception as e:
			errors.append(f"Data de fim inválida ou formato incorreto (esperado YYYY-MM-DD). Erro: {str(e)}")
		
		# Validações lógicas
		if di and df:
			if df <= di:
				errors.append("Data de fim deve ser posterior à data de início.")
			if di < date.today():
				errors.append("Data de início não pode ser anterior a hoje.")
			
			# ✅ ADICIONAL: Validar período mínimo (opcional)
			if (df - di).days < 1:
				errors.append("Período de reserva deve ser de pelo menos 1 dia.")
		
		return (len(errors) == 0), errors

	def _normalizar_data(self, data_input):
		"""
		✅ CORREÇÃO: Conversão robusta de qualquer formato de data para date
		"""
		try:
			if data_input is None:
				print(f"   ⚠️  Data é None")
				return None
			elif isinstance(data_input, str):
				# Remover possível timestamp (ex: "2025-01-15T00:00:00" → "2025-01-15")
				data_str = data_input.split('T')[0] if 'T' in data_input else data_input
				return datetime.strptime(data_str, "%Y-%m-%d").date()
			elif isinstance(data_input, datetime):
				return data_input.date()
			elif isinstance(data_input, date):
				return data_input
			else:
				print(f"   ⚠️  Tipo de data não reconhecido: {type(data_input)} - valor: {data_input}")
				return None
		except Exception as e:
			print(f"   ⚠️  Erro ao normalizar data '{data_input}': {e}")
			return None

	def _existe_sobreposicao(self, idHotel, inicio, fim, idReserva_ignorar=None):
		"""
		✅ MELHORADO: Verificação de sobreposição com logs detalhados
		"""
		print(f"🔍 Verificando sobreposição para hotel {idHotel}")
		
		# Normalizar datas de entrada
		di = self._normalizar_data(inicio)
		df = self._normalizar_data(fim)
		
		if not di or not df:
			print("   ⚠️  Erro ao normalizar datas de entrada")
			return False

		print(f"   📅 Período a verificar: {di} até {df}")

		# Buscar todas as reservas do hotel
		try:
			reservas = self.__ReservaDAO.findByField("idHotel", idHotel)
			print(f"   📋 Encontradas {len(reservas)} reservas para este hotel")
		except Exception as e:
			print(f"   ⚠️  Erro ao buscar reservas: {e}")
			return False
		
		for r in reservas:
			# Ignorar a própria reserva no caso de update
			if idReserva_ignorar and r.get("idReserva") == idReserva_ignorar:
				print(f"   ⏭️  Ignorando reserva {r.get('idReserva')} (própria reserva)")
				continue
			
			# Normalizar datas do banco
			ri = self._normalizar_data(r.get("inicio"))
			rf = self._normalizar_data(r.get("fim"))
			
			if not ri or not rf:
				print(f"   ⚠️  Erro ao normalizar datas da reserva {r.get('idReserva')}")
				continue
			
			print(f"   🔄 Comparando com reserva {r.get('idReserva')}: {ri} até {rf}")
			
			# ✅ LÓGICA CORRETA: Verifica se há sobreposição
			# (inicio < fim_existente) AND (fim > inicio_existente)
			if (di < rf) and (df > ri):
				print(f"   ⚠️  SOBREPOSIÇÃO DETECTADA com reserva {r.get('idReserva')}")
				print(f"      Nova reserva: {di} → {df}")
				print(f"      Reserva existente: {ri} → {rf}")
				return True
		
		print("   ✅ Nenhuma sobreposição encontrada")
		return False

	def findAll(self) -> list[dict]:
		print("🟣 ReservaService.findAll()")
		reservas = self.__ReservaDAO.findAll()
		print(f"   📊 Retornando {len(reservas)} reservas")
		return reservas

	def findById(self, idReserva: int) -> dict | None:
		print(f"🟣 ReservaService.findById({idReserva})")
		reserva = self.__ReservaDAO.findById(idReserva)
		
		if reserva:
			print(f"   ✅ Reserva encontrada: {reserva}")
		else:
			print(f"   ❌ Reserva não encontrada")
		
		return reserva

	def updateReserva(self, idReserva: int, jsonReserva: dict) -> bool:
		print("🟣 ReservaService.updateReserva()")
		print(f"   📦 idReserva: {idReserva}")
		print(f"   📦 jsonReserva: {jsonReserva}")
		
		try:
			reserva = Reserva()
			reserva.idReserva = idReserva
			reserva.idHospede = jsonReserva.get("idHospede")
			reserva.idHotel = jsonReserva.get("idHotel")
			reserva.inicio = jsonReserva.get("inicio")
			reserva.fim = jsonReserva.get("fim")
			
			print(f"   ✅ Objeto Reserva criado com sucesso")

			# Validações de chaves estrangeiras
			print(f"   🔍 Validando idHospede: {reserva.idHospede}")
			if not self.__HospedeDAO.findById(reserva.idHospede):
				raise ErrorResponse(400, "Hospede não encontrado", {"message": f"idHospede {reserva.idHospede} não existe"})
			
			print(f"   🔍 Validando idHotel: {reserva.idHotel}")
			if not self.__HotelDAO.findById(reserva.idHotel):
				raise ErrorResponse(400, "Hotel não encontrado", {"message": f"idHotel {reserva.idHotel} não existe"})
			
			# Validação de datas
			print(f"   🔍 Validando datas: {reserva.inicio} até {reserva.fim}")
			valid, errors = self._validar_datas(reserva.inicio, reserva.fim)
			if not valid:
				print(f"   ❌ Erros de validação: {errors}")
				raise ErrorResponse(400, "Erro de validação de datas", {"errors": errors})
			
			# ✅ CORREÇÃO CRÍTICA: Verificar sobreposição ignorando a própria reserva
			print(f"   🔍 Verificando sobreposição (ignorando reserva {idReserva})...")
			if self._existe_sobreposicao(reserva.idHotel, reserva.inicio, reserva.fim, idReserva):
				raise ErrorResponse(400, "Conflito de reserva", {"message": "Já existe uma reserva para este hotel neste período."})

			print(f"   💾 Atualizando no banco de dados...")
			resultado = self.__ReservaDAO.update(reserva)
			print(f"   ✅ Atualização concluída: {resultado}")
			return resultado
			
		except ErrorResponse as er:
			print(f"   ❌ ErrorResponse capturado: {er}")
			raise
		except Exception as e:
			print(f"   ❌ Erro não tratado em updateReserva: {type(e).__name__}: {str(e)}")
			import traceback
			traceback.print_exc()
			raise

	def deleteReserva(self, idReserva: int) -> bool:
		print(f"🟣 ReservaService.deleteReserva({idReserva})")
		
		# ✅ ADICIONAL: Verificar se reserva existe antes de deletar
		reserva_existe = self.__ReservaDAO.findById(idReserva)
		if not reserva_existe:
			print(f"   ❌ Reserva {idReserva} não encontrada para deletar")
			return False
		
		reserva = Reserva()
		reserva.idReserva = idReserva
		resultado = self.__ReservaDAO.delete(reserva)
		
		if resultado:
			print(f"   ✅ Reserva {idReserva} deletada com sucesso")
		else:
			print(f"   ❌ Falha ao deletar reserva {idReserva}")
		
		return resultado