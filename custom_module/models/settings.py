#-- coding: utf-8 --

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    module_stock_module = fields.Boolean(string="Stock Transport")
    