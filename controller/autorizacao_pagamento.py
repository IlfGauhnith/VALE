from flask import request, Flask
from flask_restful import Resource
from script.consulta_sefaz import consultar_distribuicao_chave
from business.autorizacao_pagamento import AutorizacaoPagamentoBusiness

class AutorizacaoPagamentoResource(Resource):
    def __init__(self, app: Flask, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.autorizacao_bo = AutorizacaoPagamentoBusiness(app)

    def post(self):
        if not request.is_json:
            return {'message': 'Invalid JSON format'}, 400
        
        data = request.json
        
        if 'chavesDeAcesso' not in data or not isinstance(data['chavesDeAcesso'], list):
            return {'message': 'Missing or invalid "chavesDeAcesso" array in JSON data'}, 400
        
        chaves_de_acesso = data['chavesDeAcesso']
        xmls = consultar_distribuicao_chave(self.app, chaves_de_acesso)
        for xml in xmls:
            self.autorizacao_bo.xml_to_item_autorizacao(xml)
        
        return {'nfe': xmls}, 200