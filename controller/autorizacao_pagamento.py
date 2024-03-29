from flask import request, Flask
from flask_restful import Resource
import script.consulta_sefaz as consulta_sefaz
from business.autorizacao_pagamento import AutorizacaoPagamentoBusiness
from business.nota import NotaFiscalBusiness
from model.nota import NotaFiscal
from model.autorizacao_pagamento import ItemAutorizacaoPagamento

class AutorizacaoPagamentoResource(Resource):
    def __init__(self, app: Flask, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.autorizacao_bo = AutorizacaoPagamentoBusiness(app)
        self.nota_bo = NotaFiscalBusiness(app)

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
        
        if 'modelo' not in data or not isinstance(data['modelo'], str):
            return {'message': 'Missing or invalid "modelo" string in JSON data'}, 400
        if data['modelo'] not in ['nfe', 'nfce']:
            return {'message': 'Invalid "modelo" in JSON data'}, 400
        
        chaves_acesso = data['chaves_acesso']
        modelo = data['modelo']
        
        for chave in chaves_acesso:
            _ = consulta_sefaz.manifestar_nota(self.app, modelo, chave, 1)
            xml = consulta_sefaz.consultar_distribuicao(self.app, chave)
            
            nota_fiscal:NotaFiscal = self.nota_bo.xml_to_nota_fiscal(xml)
            item_autorizacao = ItemAutorizacaoPagamento(nota_fiscal, "DESPESA1")
            
            file_path = self.autorizacao_bo.do_excel_autorizacao_pagamento(item_autorizacao)
            
        return {'directories': [file_path]}
