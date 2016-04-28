# -*- coding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 OpenPyme - http://www.openpyme.mx/
#    All Rights Reserved.
#    Coded by: Agustín Cruz (agustin.cruz@openpyme.mx)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp.osv import orm


class account_tax_code(orm.Model):
    _inherit = 'account.tax'

    def get_tax_from_rate(
        self, cr, uid, rate, is_tax_included=False, context=None
    ):
        # TODO improve, if tax are not correctly mapped the order should
        # be in exception (integration with sale_execption)
        account_tax_obj = self.pool['account.tax']
        tax_ids = account_tax_obj.search(
            cr, uid,
            [('price_include', '=', is_tax_included),
             ('type_tax_use', 'in', ['sale', 'all']),
             ('amount', '>=', rate - 0.001),
             ('amount', '<=', rate + 0.001)],
            context=context
        )
        if tax_ids:
            return tax_ids[0]
        else:
            # try to find a tax with less precision
            tax_ids = account_tax_obj.search(
                cr, uid,
                [('price_include', '=', is_tax_included),
                 ('type_tax_use', 'in', ['sale', 'all']),
                 ('amount', '>=', rate - 0.01),
                 ('amount', '<=', rate + 0.01)],
                context=context
            )
            if tax_ids:
                return tax_ids[0]
        return False
