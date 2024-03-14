from flask import request, Flask
from flask_restful import Resource
import script.consulta_sefaz as consulta_sefaz
from business.autorizacao_pagamento import AutorizacaoPagamentoBusiness

class AutorizacaoPagamentoResource(Resource):
    def __init__(self, app: Flask, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.autorizacao_bo = AutorizacaoPagamentoBusiness(app)

    def post(self):
        if not request.is_json:
            return {'message': 'Invalid JSON format'}, 400
        
        action = request.args.get('action')
        data = request.json
        
        if action == 'gerar_autorizacao':
            return self.gerar_autorizacao(data)
        
        else:
            return {'message': 'Invalid action'}, 400
                    
    def gerar_autorizacao(self, data:dict):
        if 'chaves_acesso' not in data or not isinstance(data['chaves_acesso'], list):
            return {'message': 'Missing or invalid "chaves_acesso" array in JSON data'}, 400
        
        xmls = []
        chaves_acesso = data['chaves_acesso']
        
        for chave in chaves_acesso:
            xml = consulta_sefaz.consultar_distribuicao(self.app, chave)
            xmls.append(xml)

        return {'nfe': xmls}, 200
