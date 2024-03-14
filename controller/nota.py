from flask import request, Flask
from flask_restful import Resource
import script.consulta_sefaz as consulta_sefaz

class NotaResource(Resource):
    def __init__(self, app: Flask, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        
    def post(self):
        if not request.is_json:
            return {'message': 'Invalid JSON format'}, 400
        
        action = request.args.get('action')
        data = request.json
        
        if action == 'consultar_status_nota':
            return self.consultar_status_nota(data)

        elif action == 'manifestar_nota':
            return self.manifestar_nota(data)
        
        else:
            return {'message': 'Invalid action'}, 400
        
    def consultar_status_nota(self, data:dict):
        if 'chave_acesso' not in data or not isinstance(data['chave_acesso'], str):
            return {'message': 'Missing or invalid "chave_acesso" string in JSON data'}, 400
        
        if 'modelo' not in data or not isinstance(data['modelo'], str):
            return {'message': 'Missing or invalid "modelo" string in JSON data'}, 400
        if data['modelo'] not in ['nfe', 'nfce']:
            return {'message': 'Invalid "modelo" in JSON data'}, 400
        
        
        chave_acesso = data['chave_acesso']
        modelo = data['modelo']
        xml = consulta_sefaz.consultar_nota(self.app, modelo, chave_acesso)

        return {'nfe': xml}, 200

    def manifestar_nota(self, data:dict):
        """
        operacao
            (código 1) Confirmação da Operação – confirmando a ocorrência da operação e o recebimento da mercadoria 
                (para as operações com circulação de mercadoria);
            
            (código 2) Ciência da Emissão (ou Ciência da Operação) – declarando ter ciência da operação destinada ao CNPJ, 
                mas ainda não possuir elementos suficientes para apresentar uma manifestação conclusiva, como as acima citadas. 
                Este evento era chamado de Ciência da Operação.
            
            (código 3) Desconhecimento da Operação – declarando o desconhecimento da operação;
            
            (código 4) Operação Não Realizada – declarando que a operação não foi realizada 
                (com recusa do Recebimento da mercadoria e outros) e a justificativa do porquê a operação não se realizou;
        """
        
        if 'chave_acesso' not in data or not isinstance(data['chave_acesso'], str):
            return {'message': 'Missing or invalid "chave_acesso" string in JSON data'}, 400
        
        if 'operacao' not in data or not isinstance(data['operacao'], int):
            return {'message': 'Missing or invalid "operacao" integer in JSON data'}, 400
        if data['operacao'] not in [1, 2, 3, 4]:
            return {'message': 'Invalid "operacao" in JSON data'}, 400
        
        if 'modelo' not in data or not isinstance(data['modelo'], str):
            return {'message': 'Missing or invalid "modelo" string in JSON data'}, 400
        if data['modelo'] not in ['nfe', 'nfce']:
            return {'message': 'Invalid "modelo" in JSON data'}, 400
        
        
        chave_acesso = data['chave_acesso']
        operacao = data['operacao']
        modelo = data['modelo']
        
        xml = consulta_sefaz.manifestar_nota(self.app, modelo, chave_acesso, operacao)
        return {'nfe': xml}, 200
