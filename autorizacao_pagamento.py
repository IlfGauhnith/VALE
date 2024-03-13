from flask import request, Flask
from flask_restful import Resource
from nfe import consultar_dfe

class AutorizacaoPagamentoResource(Resource):
    def __init__(self, app: Flask, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

    def post(self):
        if not request.is_json:
            return {'message': 'Invalid JSON format'}, 400
        
        data = request.json
        
        if 'chavesDeAcesso' not in data or not isinstance(data['chavesDeAcesso'], list):
            return {'message': 'Missing or invalid "chavesDeAcesso" array in JSON data'}, 400
        
        chaves_de_acesso = data['chavesDeAcesso']
        
        for chave in chaves_de_acesso:    
            nfe_xml = consultar_dfe(self.app, chave)
            
        return {'nfe': nfe_xml}, 200