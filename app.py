from flask import Flask
from flask_restful import Api
from controller.autorizacao_pagamento import AutorizacaoPagamentoResource

app = Flask(__name__)
api = Api(app)
api.add_resource(AutorizacaoPagamentoResource, '/autorizacao-pagamento', resource_class_kwargs={'app': app})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
