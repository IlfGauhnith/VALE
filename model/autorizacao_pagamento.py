from model.nota import NotaFiscal

class ItemAutorizacaoPagamento:

    def __init__(self, nota_fiscal:NotaFiscal, nome:str):
        self.nota_fiscal = nota_fiscal
        self.nome = nome
