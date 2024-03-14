from pynfe.utils.flags import NAMESPACE_NFE
from model.autorizacao_pagamento import ItemAutorizacaoPagamento
from flask import Flask

class AutorizacaoPagamentoBusiness:
    def __init__(self, app:Flask):
        self.app = app

    def do_excel_autorizacao_pagamento(self, itens:list[ItemAutorizacaoPagamento]):
        for item in itens:
            self.app.logger.info(item.fornecedor)
            self.app.logger.info(item.data_emissao)
            self.app.logger.info(item.valor)

    def xml_to_item_autorizacao(self, xml):
        ns = {'ns': NAMESPACE_NFE}
        
        print(type(xml))
