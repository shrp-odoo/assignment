#-- coding: utf-8 --

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    volume = fields.Float(string="Volume", compute="_compute_volume", default=0)

    @api.depends("move_line_ids.product_id", "move_line_ids.product_id.volume")
    def _compute_volume(self):
        for picking in self:
            picking.volume = 0 
            for move_line in picking.move_line_ids:
                picking.volume += move_line.product_id.volume
                