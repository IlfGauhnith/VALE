from datetime import datetime

class NotaFiscal:
    
    def __init__(self, numero:str, valor:float, data_emissao:datetime, fornecedor:str, chave_acesso:str):
        self.numero =  numero
        self.valor = valor
        self.data_emissao = data_emissao
        self.fornecedor = fornecedor
        self.chave_acesso = chave_acesso

    def __str__(self):
        return f"Nota Fiscal: {self.numero}\nValor: {self.valor}\nData de Emissão: {self.data_emissao}\nFornecedor: {self.fornecedor}\nChave de Acesso: {self.chave_acesso}"