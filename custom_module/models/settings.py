#-- coding: utf-8 --

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    stock_module = fields.Boolean(string="Stock Transport")
    