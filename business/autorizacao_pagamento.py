from pynfe.utils.flags import NAMESPACE_NFE
from model.autorizacao_pagamento import ItemAutorizacaoPagamento
from script.file import copy_to_temp
from flask import Flask
import os
from openpyxl import load_workbook
from datetime import datetime
from dateutil.relativedelta import relativedelta

class AutorizacaoPagamentoBusiness:
    def __init__(self, app:Flask):
        self.app = app

    def do_excel_autorizacao_pagamento(self, item_autorizacao:ItemAutorizacaoPagamento):
        temp_file_path = copy_to_temp(self.app, os.path.join("resource", "template_autorizacao_pagamento.xlsx"), "autorizacao1.xlsx")
        workbook = load_workbook(temp_file_path)
        
        worksheet = workbook.active
        
        worksheet['B1'] = "BURLE CAFETERIA LTDA"
        worksheet['B2'] = "52.241.518/0001-10"
        worksheet['B5'] = datetime.now().strftime("%d-%m-%Y")
        worksheet['E2'] = "DEL-LUZ-PE"
        
        worksheet['A10'] = f"{item_autorizacao.nome}/{item_autorizacao.nota_fiscal.fornecedor}"
        worksheet['B10'] = item_autorizacao.nota_fiscal.data_emissao.strftime("%d-%m-%Y")
        worksheet['C10'] = item_autorizacao.nota_fiscal.numero
        
        worksheet['C14'] = (item_autorizacao.nota_fiscal.data_emissao + relativedelta(months=1)).strftime("%d-%m-%Y")
        worksheet['D14'] = item_autorizacao.nota_fiscal.valor
        
        workbook.save(temp_file_path)
        return temp_file_path