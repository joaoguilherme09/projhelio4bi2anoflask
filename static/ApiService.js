/**
 * Classe ApiService para facilitar chamadas HTTP (GET, POST, PUT, DELETE) a APIs RESTful.
 * Suporta autenticação via token Bearer e fornece métodos reutilizáveis para diferentes tipos de requisições.
 */
export default class ApiService {
    #token;    // Atributo privado para armazenar o token de autenticação
    #baseURL;  // Atributo privado para armazenar a URL base da API

    /**
     * Construtor da classe ApiService.
     * @param {string|null} token - Token de autenticação opcional para incluir no header Authorization.
     * @param {string} baseURL - URL base da API (ex: "http://127.0.0.1:8000")
     */
    constructor(token = null, baseURL = "http://127.0.0.1:8000") {
        this.#token = token;
        this.#baseURL = baseURL;
    }

    /**
     * Método para lidar com erro de autenticação
     */
    #handleAuthError() {
        console.error("❌ Erro de autenticação - redirecionando para login");
        localStorage.removeItem("token");
        localStorage.removeItem("userData");
        window.location.href = "./login.html";
    }

    /**
     * Método auxiliar para montar URL completa
     * @param {string} endpoint - Endpoint relativo (ex: "/api/v1/hospedes")
     * @returns {string} URL completa
     */
    #buildURL(endpoint) {
        return `${this.#baseURL}${endpoint}`;
    }

    /**
     * Método para verificar resposta HTTP e tratar erros de auth
     * @param {Response} response - Resposta da fetch API
     * @returns {Response} Resposta verificada
     */
    async #checkResponse(response) {
        if (response.status === 401) {
            this.#handleAuthError();
            throw new Error("Não autorizado - token inválido ou expirado");
        }
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status} - ${response.statusText}`);
        }
        
        return response;
    }

    /**
     * Método para fazer uma requisição GET simples sem headers adicionais.
     * Útil para APIs públicas que não requerem autenticação.
     * @param {string} endpoint - Endpoint do recurso para a requisição GET.
     * @returns {Promise<Object|Array>} Retorna o JSON obtido da resposta ou array vazio em caso de erro.
     */
    async simpleGet(endpoint) {
        try {
            const uri = this.#buildURL(endpoint);
            const response = await fetch(uri);
            const jsonObj = await response.json();
            console.log("GET:", uri, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("Erro ao buscar dados:", error.message);
            return [];
        }
    }

    /**
     * Método para requisição GET com headers, incluindo token se presente.
     * Usado para APIs que exigem autenticação ou headers customizados.
     * @param {string} endpoint - Endpoint do recurso para a requisição GET.
     * @returns {Promise<Object|Array>} Retorna JSON da resposta ou array vazio em caso de erro.
     */
    async get(endpoint) {
        try {
            const uri = this.#buildURL(endpoint);
            
            const headers = {
                "Content-Type": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            const response = await fetch(uri, {
                method: "GET",
                headers: headers
            });

            await this.#checkResponse(response);
            const jsonObj = await response.json();
            console.log("GET:", uri, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("Erro ao buscar dados:", error.message);
            
            if (error.message.includes("Não autorizado")) {
                return { success: false, error: { message: "Sessão expirada" } };
            }
            
            return { success: false, error: { message: error.message } };
        }
    }

    /**
     * Método para buscar um recurso específico pelo ID via GET.
     * Monta a URL com o ID no final e faz a requisição.
     * @param {string} endpoint - Endpoint base do recurso.
     * @param {string|number} id - Identificador do recurso a ser buscado.
     * @returns {Promise<Object|null>} Retorna JSON do recurso ou null em caso de erro.
     */
    async getById(endpoint, id) {
        try {
            const uri = this.#buildURL(`${endpoint}/${id}`);
            
            const headers = {
                "Content-Type": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            const response = await fetch(uri, {
                method: "GET",
                headers: headers
            });

            await this.#checkResponse(response);
            const jsonObj = await response.json();
            console.log("GET BY ID:", uri, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("Erro ao buscar por ID:", error.message);
            
            if (error.message.includes("Não autorizado")) {
                return { success: false, error: { message: "Sessão expirada" } };
            }
            
            return { success: false, error: { message: error.message } };
        }
    }

    /**
     * Método para enviar dados via POST para criar um novo recurso.
     * Envia o objeto JSON serializado no corpo da requisição.
     * @param {string} endpoint - Endpoint para POST.
     * @param {Object} jsonObject - Objeto a ser enviado como corpo JSON.
     * @returns {Promise<Object|Array>} Retorna JSON da resposta ou array vazio em caso de erro.
     */
    async post(endpoint, jsonObject) {
        try {
            const uri = this.#buildURL(endpoint);
            
            const headers = {
                "Content-Type": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            const response = await fetch(uri, {
                method: "POST",
                headers: headers,
                body: JSON.stringify(jsonObject)
            });

            await this.#checkResponse(response);
            const jsonObj = await response.json();
            console.log("POST:", uri, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("Erro ao enviar dados POST:", error.message);
            
            if (error.message.includes("Não autorizado")) {
                return { success: false, error: { message: "Sessão expirada" } };
            }
            
            return { success: false, error: { message: error.message } };
        }
    }

    /**
     * Método para atualizar um recurso via PUT usando ID e objeto JSON.
     * @param {string} endpoint - Endpoint base do recurso.
     * @param {string|number} id - ID do recurso a ser atualizado.
     * @param {Object} jsonObject - Dados atualizados a serem enviados no corpo da requisição.
     * @returns {Promise<Object|null>} Retorna JSON da resposta ou null em caso de erro.
     */
    async put(endpoint, id, jsonObject) {
        try {
            const uri = this.#buildURL(`${endpoint}/${id}`);
            
            const headers = {
                "Content-Type": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            const response = await fetch(uri, {
                method: "PUT",
                headers: headers,
                body: JSON.stringify(jsonObject)
            });

            await this.#checkResponse(response);
            const jsonObj = await response.json();
            console.log("PUT:", uri, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("Erro ao enviar dados PUT:", error.message);
            
            if (error.message.includes("Não autorizado")) {
                return { success: false, error: { message: "Sessão expirada" } };
            }
            
            return { success: false, error: { message: error.message } };
        }
    }

    /**
     * Método para deletar um recurso via DELETE usando ID.
     * @param {string} endpoint - Endpoint base do recurso.
     * @param {string|number} id - ID do recurso a ser deletado.
     * @returns {Promise<Object|null>} Retorna JSON da resposta ou null se não houver corpo ou erro.
     */
    async delete(endpoint, id) {
        try {
            const uri = `${this.#baseURL}${endpoint}/${id}`;
            
            const headers = {
                "Content-Type": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            console.log("DELETE:", uri);
            const response = await fetch(uri, {
                method: "DELETE",
                headers: headers
            });

            await this.#checkResponse(response);

            let jsonObj = null;
            
            // ✅ CORREÇÃO: Verificar se há conteúdo antes de tentar parsear
            const content = await response.text();
            
            if (content && content.trim() !== '') {
                try {
                    jsonObj = JSON.parse(content);
                } catch (e) {
                    console.log("❌ Erro ao parsear resposta DELETE:", e);
                    // Se não conseguir parsear mas a resposta foi bem-sucedida, considerar sucesso
                    if (response.ok) {
                        jsonObj = { success: true, message: "Deletado com sucesso" };
                    } else {
                        throw new Error("Resposta inválida do servidor");
                    }
                }
            } else {
                // ✅ CORREÇÃO: Se não há conteúdo mas status é OK, considerar sucesso
                if (response.ok) {
                    jsonObj = { success: true, message: "Deletado com sucesso" };
                } else {
                    throw new Error("Resposta vazia do servidor");
                }
            }

            console.log("DELETE:", uri, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("❌ Erro ao deletar dados:", error.message);
            
            if (error.message.includes("Não autorizado")) {
                return { success: false, error: { message: "Sessão expirada" } };
            }
            
            return { success: false, error: { message: error.message } };
        }
    }

    /**
     * Verificar se o token é válido (para JWT)
     * @returns {boolean} True se o token for válido
     */
    isTokenValid() {
        if (!this.#token) return false;
        
        try {
            // Para tokens JWT, verificar expiração
            if (this.#token.includes('.')) {
                const payload = JSON.parse(atob(this.#token.split('.')[1]));
                return payload.exp * 1000 > Date.now();
            }
            return true; // Para tokens não-JWT, assumir válido
        } catch {
            return false;
        }
    }

    /**
     * Getter para o token privado.
     * @returns {string|null} Retorna o token atual.
     */
    get token() {
        return this.#token;
    }

    /**
     * Setter para atualizar o token privado.
     * @param {string} value - Novo token a ser setado.
     */
    set token(value) {
        this.#token = value;
    }

    /**
     * Getter para a URL base.
     * @returns {string} Retorna a URL base atual.
     */
    get baseURL() {
        return this.#baseURL;
    }

    /**
     * Setter para atualizar a URL base.
     * @param {string} value - Nova URL base a ser setada.
     */
    set baseURL(value) {
        this.#baseURL = value;
    }
}