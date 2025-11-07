class ErrorResponse(Exception):
    def __init__(self, httpCode: int, message: str, error: any = None):
        super().__init__(message)
        self._httpCode = httpCode  
        self._error = error  
        
    # Getter para o código HTTP
    def getHttpCode(self) -> int:  
        return self._httpCode
    
    # Getter para a mensagem
    def getMessage(self) -> str:  
        return self.args[0]
    
    # Getter para o erro detalhado
    def getError(self):  
        return self._error

    # Representação em string
    def __str__(self) -> str:
        return f"[{self._httpCode}] {self.args[0]} | Detalhes: {self._error}"