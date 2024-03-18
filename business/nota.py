from pynfe.utils.flags import NAMESPACE_NFE
from model.nota import NotaFiscal
from datetime import datetime
from flask import Flask
import lxml

class NotaFiscalBusiness:
    def __init__(self, app:Flask):
        self.app = app
    
    def xml_to_nota_fiscal(self, xml:lxml.etree._Element):
        ns = {'ns': NAMESPACE_NFE}

        numero = xml.xpath('//ns:nfeProc/ns:NFe/ns:infNFe/ns:ide/ns:nNF', namespaces=ns)[0].text
        valor = float(xml.xpath('//ns:nfeProc/ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vProd', namespaces=ns)[0].text)
        data_emissao = datetime.strptime(xml.xpath('//ns:nfeProc/ns:NFe/ns:infNFe/ns:ide/ns:dhEmi', namespaces=ns)[0].text, "%Y-%m-%dT%H:%M:%S%z") 
        fornecedor = xml.xpath('//ns:nfeProc/ns:NFe/ns:infNFe/ns:emit/ns:xNome', namespaces=ns)[0].text
        chave_acesso = xml.xpath('//ns:nfeProc/ns:protNFe/ns:infProt/ns:chNFe', namespaces=ns)[0].text

        nota_fiscal = NotaFiscal(numero, valor, data_emissao, fornecedor, chave_acesso)
        
        return nota_fiscal