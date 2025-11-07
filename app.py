from server import Server
"""
Arquivo principal de inicialização do servidor Flask.

Responsabilidades:
- Cria a instância do servidor
- Inicializa todas as dependências (banco, middlewares, rotas)
- Inicia o servidor na porta especificada
"""
def main():
    try:
        # Cria instância do servidor na porta 8000
        server = Server(porta=8000)

        # Inicializa servidor (DB, middlewares, roteadores)
        server.init()

        # Inicia servidor Flask
        server.run()

        print("✅ Servidor iniciado com sucesso")
    except Exception as error:
        print("❌ Erro ao iniciar o servidor:", error)



main()