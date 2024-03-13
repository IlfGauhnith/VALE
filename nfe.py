from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from flask import Flask
from xml.etree import ElementTree
import os

certificado_path = os.path.join('burle.pfx')
print(certificado_path)
senha = '123456'
uf = 'pe'
CNPJ = '52241518000110'
homologacao = False

def status_sefaz(app:Flask, modelo):
    con = ComunicacaoSefaz(uf, certificado_path, senha, homologacao)
    xml = con.status_servico(modelo)
    
    ns = { 'ns': NAMESPACE_NFE }
    resposta = etree.fromstring(xml.content)[0][0]

    status = resposta.xpath('ns:retConsStatServ/ns:cStat', namespaces=ns)[0].text
    
    app.logger.info(f"Status do serviço {modelo} sefaz: {status}")
    
    return status == '107'

def status_nota(app:Flask, chave_acesso, modelo):
    if status_sefaz(app):
        con = ComunicacaoSefaz(uf, certificado_path, senha, homologacao)
        response = con.consulta_nota(modelo, chave_acesso)
        
        ns = {'ns': NAMESPACE_NFE}
        prot = etree.fromstring(response.text.encode('utf-8'))
        status = prot[0][0].xpath('ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text
        
        return response.text
    else:
        pass #TODO Throw sefaz service not available exception.

def consultar_dfe(app:Flask, chave_acesso):
    con = ComunicacaoSefaz(uf, certificado_path, senha, homologacao)
    xml = con.consulta_distribuicao(cnpj=CNPJ, chave='', nsu=int(chave_acesso), consulta_nsu_especifico=True)
    resposta = etree.fromstring(xml.content)
    ns = {'ns': NAMESPACE_NFE}

    zip_resposta = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
    des_resposta = DescompactaGzip.descompacta(zip_resposta)
    
    return ElementTree.tostring(des_resposta, encoding='unicode')
