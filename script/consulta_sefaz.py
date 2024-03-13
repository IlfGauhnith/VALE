from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from lxml import etree
from flask import Flask
import os

certificado_path = os.path.join('burle.pfx')
senha = '123456'
uf = 'pe'
CNPJ = '52241518000110'
homologacao = False

def consultar_distribuicao_chave(app:Flask, chaves:list[str]):
    con = ComunicacaoSefaz(uf, certificado_path, senha, homologacao)
    ns = {'ns': NAMESPACE_NFE}
    xmls = []

    for chave in chaves:
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
                xmls.append(resposta_descompactado)   

            elif (docZip_schema == 'resNFe_v1.01.xsd'):
                zip_resposta = xml_etree.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
                resposta_descompactado = DescompactaGzip.descompacta(zip_resposta)
                xmls.append(resposta_descompactado)

        else:
            pass


    return xmls


