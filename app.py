from flask import Flask, send_file
from flask_restful import Api
from flask_cors import CORS
from controller.autorizacao_pagamento import AutorizacaoPagamentoResource
from controller.nota import NotaResource
from zipfile import ZipFile
from io import BytesIO
import os

def response_octet_stream_file(data, code, headers):

    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for directory in data['directories']:
            filepath = os.path.join(directory)
            zf.write(filepath, os.path.basename(filepath))
    stream.seek(0)

    response = send_file(
        path_or_file=stream,
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='archive.zip'
    )
    
    return response

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(AutorizacaoPagamentoResource, '/autorizacao-pagamento', resource_class_kwargs={'app': app})
api.add_resource(NotaResource, '/nota', resource_class_kwargs={'app': app})
api.representations['application/octet-stream'] = response_octet_stream_file

if __name__ == '__main__':
    app.run(debug=True, port=5004)
