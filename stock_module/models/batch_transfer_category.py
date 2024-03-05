#-- coding: utf-8 --

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(string="Volume", compute="_compute_volume")

    @api.depends("product_id")
    def _compute_volume(self):
        v = 0
        for move_line in self.move_line_ids:
            v += move_line.product_id.volume

        self.volume = v
