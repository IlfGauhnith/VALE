from pynfe.utils.flags import NAMESPACE_NFE
from model.autorizacao_pagamento import ItemAutorizacaoPagamento
from flask import Flask

class AutorizacaoPagamentoBusiness:
    def __init__(self, app:Flask):
        self.app = app

    def do_excel_autorizacao_pagamento(self, itens:list[ItemAutorizacaoPagamento]):
        pass