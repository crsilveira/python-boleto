# -*- coding: utf-8 -*-
from pyboleto.data import BoletoData, CustomProperty


class BoletoSicredi(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o Banco Sicredi
    '''
    agencia_cedente = CustomProperty('agencia_cedente', 4)
    conta_cedente = CustomProperty('conta_cedente', 8)
    posto = CustomProperty('posto', 2)
    carteira = CustomProperty('carteira', 1)
    convenio = CustomProperty('convenio', 15017)
    # Nosso numero (sem dv) com 8 digitos
    # AA/BXXXXX-DV 
    # Pag. 6 manual cnab 400
    nosso_numero = CustomProperty('nosso_numero', 8)

    def __init__(self):
        '''
            Construtor para boleto do Banco Sicredi

            Args:
                format_convenio Formato do convenio 6, 7 ou 8
                format_nnumero Formato nosso numero 1 ou 2
        '''
        super(BoletoSicredi, self).__init__()

        self.codigo_banco = "748"
        self.local_pagamento = u'Pagável prefencialmente nas Coop. de Crédito Sicredi'
        self.logo_image = "logo_sicredi.png"

        # Size of convenio 6, 7 or 8
        self.format_convenio = 5
        self.posto = '00' 

        #  Nosso Numero format. 1 or 2
        #  1: Nosso Numero with 5 positions
        #  2: Nosso Numero with 17 positions
        self.format_nnumero = 1  # self.nosso_numero

    def format_ano(self):
        ano = str(self.data_documento.strftime('%y'))
        ano = ano.zfill(2)
        #ano = 24
        return ano

    def format_nosso_numero(self):

        # 14 ano + 2 : Nosso Número deve ser apresentado no formato
        # AA/BXXXXX-D, onde:
        return "%s/3%s-%s" % (
            self.format_ano(),
            self.nosso_numero,
            self.dv_nosso_numero
        )

    # Nosso numero (sem dv) sao 11 digitos
    def _get_nosso_numero(self):
        return self._nosso_numero

    def _set_nosso_numero(self, val):
        val = str(val)
        if self.format_convenio == 5:
            if self.format_nnumero == 1:
                nn = val.zfill(5)
            elif self.format_nnumero == 2:
                nn = val.zfill(17)
        elif self.format_convenio == 7:
            nn = val.zfill(10)
        elif self.format_convenio == 8:
            nn = val.zfill(9)
        self._nosso_numero = nn

    nosso_numero = property(_get_nosso_numero, _set_nosso_numero)

    def _get_convenio(self):
        return self._convenio

    def _set_convenio(self, val):
        self._convenio = str(val).rjust(self.format_convenio, '0')
    convenio = property(_get_convenio, _set_convenio)

    @property
    def agencia_conta_cedente(self):
        return "%s.%s.%s" % (
            self.agencia_cedente[:self.agencia_cedente.find('-')],
            self.dv_agencia,
            self.convenio
        )

    @property
    def dv_nosso_numero(self):
        dv = "%s%s%s%s3%s" % (self.agencia_cedente[:self.agencia_cedente.find('-')],
                              self.dv_agencia,
                              self.convenio,
                              self.format_ano(),
                              self.nosso_numero
                              )
        dv = self.modulo11(dv)
        return dv

    @property
    def campo_livre(self):
        content = str("")
        if self.format_nnumero == 1:
            #        "3027050000414205586")
            # 14 ano + 2 : Nosso Número deve ser apresentado no formato
            # AA/BXXXXX-D, onde:
            content = "%s1%s3%s%s%s%s%s10" % (self.carteira,
                                              self.format_ano(),
                                              self.nosso_numero,
                                              self.dv_nosso_numero,
                                              self.agencia_cedente[:self.agencia_cedente.find('-')],
                                              self.dv_agencia,
                                              self.convenio
                                              )
            n = self.modulo11(content)
            if n > 9:
                n = 1
            content += str(n)
        return str(content)

    @property
    def codigo_dv_banco(self):
        cod = "%s-X" % (self.codigo_banco)
        return cod
