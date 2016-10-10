#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# test_bormeregexp.py -
# Copyright (C) 2015 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from bormeparser.regex import regex_cargos, regex_empresa, regex_bold_acto, is_company
from bormeparser.regex import is_acto_cargo_entrante, regex_empresa_tipo, borme_c_separa_empresas_titulo




class BormeparserIsCompanyTestCase(unittest.TestCase):
    empresa1 = 'PATATAS SL'
    empresa2 = 'HAMBURGUESAS AIE'
    empresa3 = 'ZANAHORIAS SA'
    empresa4 = 'COA-COA BARBACOA SRL'
    persona1 = 'JOHN DOE'

    def test_is_company(self):
        self.assertTrue(is_company(self.empresa1))
        self.assertTrue(is_company(self.empresa2))
        self.assertTrue(is_company(self.empresa3))
        self.assertTrue(is_company(self.empresa4))
        self.assertFalse(is_company(self.persona1))


class BormeparserRegexEmpresaTestCase(unittest.TestCase):
    acto1 = '57344 - ALDARA CATERING SL.'
    acto2 = '57344 - ALDARA CATERING SL'
    acto3 = u'473700 - SA COVA PLAÇA MAJOR SL(R.M. PALMA DE MALLORCA)'
    empresa1 = 'ALDARA CATERING SL'
    empresa2 = 'ALDARA CATERING'

    def test_regex_empresa(self):
        acto_id, empresa, registro = regex_empresa(self.acto1)
        self.assertEqual(acto_id, 57344)
        self.assertEqual(empresa, 'ALDARA CATERING SL')
        self.assertEqual(registro, None)

        acto_id, empresa, registro = regex_empresa(self.acto2)
        self.assertEqual(acto_id, 57344)
        self.assertEqual(empresa, 'ALDARA CATERING SL')
        self.assertEqual(registro, None)

        acto_id, empresa, registro = regex_empresa(self.acto3)
        self.assertEqual(acto_id, 473700)
        self.assertEqual(empresa, u'SA COVA PLAÇA MAJOR SL')
        self.assertEqual(registro, 'Palma de Mallorca')

    def test_regex_empresa_tipo(self):
        empresa, tipo = regex_empresa_tipo(self.empresa1)
        self.assertEqual(empresa, 'ALDARA CATERING')
        self.assertEqual(tipo, 'SL')

        empresa, tipo = regex_empresa_tipo(self.empresa2)
        self.assertEqual(empresa, 'ALDARA CATERING')
        self.assertEqual(tipo, '')


class BormeparserRegexCargosTestCase(unittest.TestCase):
    nombramientos1 = 'Adm. Solid.: RAMA SANCHEZ JOSE PEDRO;RAMA SANCHEZ JAVIER JORGE.'
    nombramientos2 = u'Auditor: ACME AUDITORES SL. Aud.Supl.: MACIAS MUÑOZ FELIPE JOSE.'
    nombramientos3 = u'Auditor: A.T.A AUDITORES SL. Aud.Supl.: CUEVAS MUÑOZ SILVIA MARIA.'
    nombramientos4 = u'Adm. Solid.: ASDFG INVERSIONES S.L. Adm. Mancom.: ASDFG INVERSIONES S.L.;PEDRO PEREZ'
    nombramientos5 = u"Apoderado: CASER PENSIONES ENTIDAD GESTORA DE FONDOS DE PENSI."

    ceses1 = u'Adm. Mancom.: PEREZ;HILARIO'
    ceses2 = u'Auditor: A.T.A AUDITORES SL. Adm. Mancom.: PEREZ;HILARIO'
    ceses3 = u"Consejero: C1 C. Consejero: C2 -A- Secretario: C2 -B- Vicesecret.: C4 -D-"

    def test_regex_nombramientos(self):
        cargos1 = regex_cargos(self.nombramientos1)
        self.assertEqual(cargos1, {'Adm. Solid.': {'RAMA SANCHEZ JAVIER JORGE', 'RAMA SANCHEZ JOSE PEDRO'}})

        cargos2 = regex_cargos(self.nombramientos2)
        self.assertEqual(cargos2, {'Auditor': {'ACME AUDITORES SL'}, 'Aud.Supl.': {u'MACIAS MUÑOZ FELIPE JOSE'}})

        cargos3 = regex_cargos(self.nombramientos3)
        self.assertEqual(cargos3, {'Auditor': {'A.T.A AUDITORES SL'}, 'Aud.Supl.': {u'CUEVAS MUÑOZ SILVIA MARIA'}})

        cargos4 = regex_cargos(self.nombramientos4)
        self.assertEqual(cargos4, {'Adm. Solid.': {'ASDFG INVERSIONES SL'},
                                   'Adm. Mancom.': {'ASDFG INVERSIONES SL', 'PEDRO PEREZ'}})

        cargos4 = regex_cargos(self.nombramientos5)
        self.assertEqual(cargos4, {'Apoderado': {'CASER PENSIONES ENTIDAD GESTORA DE FONDOS DE PENSI'}})

        ceses1 = regex_cargos(self.ceses1)
        self.assertEqual(ceses1, {'Adm. Mancom.': {'PEREZ', 'HILARIO'}})

        ceses2 = regex_cargos(self.ceses2)
        self.assertEqual(ceses2, {'Auditor': {'A.T.A AUDITORES SL'},
                                  'Adm. Mancom.': {'PEREZ', 'HILARIO'}})

        ceses3 = regex_cargos(self.ceses3)
        self.assertEqual(ceses3, {'Consejero': {'C1 C', 'C2 -A-'},
                                  'Secretario': {'C2 -B-'},
                                  'Vicesecret.': {'C4 -D-'}})


    def test_cargo_entrante(self):
        self.assertTrue(is_acto_cargo_entrante('Reelecciones'))
        self.assertTrue(is_acto_cargo_entrante('Nombramientos'))
        self.assertFalse(is_acto_cargo_entrante('Ceses/Dimisiones'))
        self.assertRaises(ValueError, is_acto_cargo_entrante, 'Cambio de domicilio social')


class BormeparserRegexBoldTestCase(unittest.TestCase):
    string1 = u'Declaración de unipersonalidad. Socio único: GRUPO DE EMPRESAS E INVERSIONES YOLO S.L. Nombramientos'
    string2 = u'Declaración de unipersonalidad. Socio único: JOHN DOE. Datos registrales'
    string3 = u'Declaración de unipersonalidad. Socio único: FOO DOE. Pérdida del caracter de unipersonalidad. Cambio de domicilio social.'
    string4 = u'Declaración de unipersonalidad. Socio único: CORPOREISHON BLA BLA. Cif:B12345678.Ceses/Dimisiones.'
    string5 = u'Declaración de unipersonalidad. Socio único: ENGLOBA GRUPO DE COMUNICACION SL. Sociedad unipersonal. Cambio de identidad del socio único: GRUPO ANTALA MEDIA SL. Datos registrales.'


    def test_regex_decl_unip(self):
        acto_colon, arg_colon, nombreacto = regex_bold_acto(self.string1)
        self.assertEqual(acto_colon, u'Declaración de unipersonalidad')
        self.assertEqual(arg_colon, u'Socio único: GRUPO DE EMPRESAS E INVERSIONES YOLO S.L')
        self.assertEqual(nombreacto, 'Nombramientos')

        acto_colon, arg_colon, nombreacto = regex_bold_acto(self.string2)
        self.assertEqual(acto_colon, u'Declaración de unipersonalidad')
        self.assertEqual(arg_colon, u'Socio único: JOHN DOE')
        self.assertEqual(nombreacto, 'Datos registrales')

        acto_colon, arg_colon, nombreacto = regex_bold_acto(self.string3)
        self.assertEqual(acto_colon, u'Declaración de unipersonalidad')
        self.assertEqual(arg_colon, u'Socio único: FOO DOE')
        self.assertEqual(nombreacto, u'Pérdida del caracter de unipersonalidad. Cambio de domicilio social.')

        acto_colon, arg_colon, nombreacto = regex_bold_acto(self.string4)
        self.assertEqual(acto_colon, u'Declaración de unipersonalidad')
        self.assertEqual(arg_colon, u'Socio único: CORPOREISHON BLA BLA. Cif:B12345678')
        self.assertEqual(nombreacto, u'Ceses/Dimisiones.')

        acto_colon, arg_colon, nombreacto = regex_bold_acto(self.string5)
        self.assertEqual(acto_colon, u'Declaración de unipersonalidad')
        self.assertEqual(arg_colon, u'Socio único: ENGLOBA GRUPO DE COMUNICACION SL')
        self.assertEqual(nombreacto, u'Sociedad unipersonal. Cambio de identidad del socio único: GRUPO ANTALA MEDIA SL. Datos registrales.')


class BormeparserRegexBormeC(unittest.TestCase):
    titulo1 = 'PARQUE EMPRESARIAL OMEGA, S.L.U, SOCIEDAD ABSORBENTE\nFGLG OMEGA 2, S.L.U.\nFGLG OMEGA 5, S.L.U.(SOCIEDADES ABSORBIDAS)'
    titulo3 = 'INDUSTRIAS TEVI, S.L.\n(SOCIEDAD ESCINDIDA)\nTEVIINMUEBLES 2009, S.L.\n(SOCIEDAD BENEFICIARIA)'
    titulo4 = 'NAVES EN ALQUILER PARA LA INDUSTRIA, S.L.\nSOCIEDAD ABSORBENTE Y\nCOCINAS RONDA NORTE, S.L.\nSOCIEDAD ABSORBIDA'
    #titulo5 = u'TÉCNICA EN INSTALACIONES DE FLUIDOS, S.L. (SOCIEDAD ABSORBENTE), MONTAJES INOXIDABLES MOINOX, S.L. UNIPERSONAL (SOCIEDAD ABSORBIDA).'
    #titulo6 = 'SOCIEDAD ANONIMA\nINDUSTRIAS CELULOSA ARAGONESA\n(SOCIEDAD ABSORBENTE)\nCABALUR, SOCIEDAD LIMITADA UNIPERSONAL\n(SOCIEDAD ABSORBIDA)'
    #titulo7 = u'SICA, S.L. (SOCIEDAD ABSORBENTE), CAOLINA, S.L. DE CARÁCTER UNIPERSONAL\n(SOCIEDAD ABSORBIDA)'

    def test_separar_empresas_titulo(self):
        empresas1 = borme_c_separa_empresas_titulo(self.titulo1)
        self.assertEqual(empresas1, ['PARQUE EMPRESARIAL OMEGA, S.L.U', 'FGLG OMEGA 2, S.L.U.', 'FGLG OMEGA 5, S.L.U.'])
        empresas3 = borme_c_separa_empresas_titulo(self.titulo3)
        self.assertEqual(empresas3, ['INDUSTRIAS TEVI, S.L.', 'TEVIINMUEBLES 2009, S.L.'])
        empresas4 = borme_c_separa_empresas_titulo(self.titulo4)
        self.assertEqual(empresas4, ['NAVES EN ALQUILER PARA LA INDUSTRIA, S.L.', 'COCINAS RONDA NORTE, S.L.'])
        #empresas5 = borme_c_separa_empresas_titulo(self.titulo5)
        #self.assertEqual(empresas5, [u'TÉCNICA EN INSTALACIONES DE FLUIDOS, S.L.', 'MONTAJES INOXIDABLES MOINOX, S.L. UNIPERSONAL'])
        #empresas6 = borme_c_separa_empresas_titulo(self.titulo6)
        #self.assertEqual(empresas6, ['SOCIEDAD ANONIMA INDUSTRIAS CELULOSA ARAGONESA', 'CABALUR, SOCIEDAD LIMITADA UNIPERSONAL'])
        #empresas7 = borme_c_separa_empresas_titulo(self.titulo7)
        #self.assertEqual(empresas7, ['SICA, S.L.', 'CAOLINA, S.L. DE CARÁCTER UNIPERSONAL'])

if __name__ == '__main__':
    unittest.main()
