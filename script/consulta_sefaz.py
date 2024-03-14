from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.entidades.evento import EventoManifestacaoDest
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.utils.flags import NAMESPACE_NFE
import datetime
from lxml import etree
from xml.etree import ElementTree
from flask import Flask
import os

certificado = os.path.join('burle.pfx')
senha = '123456'
uf = 'pe'
CNPJ = '52241518000110'
homologacao = False

def consultar_distribuicao(app:Flask, chave:str):
    ns = {'ns': NAMESPACE_NFE}
    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)

    app.logger.info(f"Documento {chave}")
    response = con.consulta_distribuicao(cnpj=CNPJ, chave=chave)
    xml_etree = etree.fromstring(response.text.encode('utf-8'))

    cStat = xml_etree.xpath('//ns:retDistDFeInt/ns:cStat', namespaces=ns)[0].text
    xMotivo = xml_etree.xpath('//ns:retDistDFeInt/ns:xMotivo', namespaces=ns)[0].text

    app.logger.info(f"cStat: {cStat}")
    app.logger.info(f"xMotivo {xMotivo}")

    if cStat == '138':
        docZip_schema = xml_etree.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip/@schema', namespaces=ns)[0]
        app.logger.info(f"docZip_schema {docZip_schema}")

        if (docZip_schema == 'procNFe_v4.00.xsd'): 
            zip_resposta = xml_etree.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
            resposta_descompactado = DescompactaGzip.descompacta(zip_resposta)
            
            xml = ElementTree.tostring(resposta_descompactado, encoding='unicode')
            #xml = resposta_descompactado

        elif (docZip_schema == 'resNFe_v1.01.xsd'):
            zip_resposta = xml_etree.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
            resposta_descompactado = DescompactaGzip.descompacta(zip_resposta)
            
            xml = ElementTree.tostring(resposta_descompactado, encoding='unicode')
            #xml = resposta_descompactado
    else:
        pass
    
    return xml

def consultar_nota(app:Flask, modelo:str, chave:str):
    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    response = con.consulta_nota(modelo, chave)
    xml_etree = etree.fromstring(response.text.encode('utf-8'))
    
    return ElementTree.tostring(xml_etree, encoding='unicode')

def manifestar_nota(app:Flask, modelo:str, chave_acesso:str, operacao:int):
    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    
    manif_dest = EventoManifestacaoDest(
	    cnpj=CNPJ,
	    chave=chave_acesso,
	    data_emissao=datetime.datetime.now(),
	    uf='AN', # AMBIENTE NACIONAL
	    operacao=operacao
    )
    
    serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
    nfe_manif = serializador.serializar_evento(manif_dest)
    
    a1 = AssinaturaA1(certificado, senha)
    xml = a1.assinar(nfe_manif)
    
    response = con.evento(modelo=modelo, evento=xml)
    xml_etree = etree.fromstring(response.text.encode('utf-8'))
    
    return ElementTree.tostring(xml_etree, encoding='unicode')
