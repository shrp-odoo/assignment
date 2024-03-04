#-- coding: utf-8 --

from odoo import api, fields, models

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    vehicle = fields.Many2one(string="Vehicle", comodel_name="fleet.vehicle")
    vehicle_category = fields.Many2one(string="Category", comodel_name="fleet.vehicle.model.category")
    weight = fields.Float(string="Weight(kg)", compute="_compute_weight", default=0)
    volume = fields.Float(string="Volume", compute="_compute_volume", default=0)

    @api.depends('vehicle_category.max_weight', 'weight')
    def _compute_weight(self):
        for record in self:
            if record.vehicle_category and record.vehicle_category.max_weight != 0:
                record.weight = record.weight / record.vehicle_category.max_weight
            else:
                record.weight = 0.0


    @api.depends('vehicle_category.max_volume', 'volume')
    def _compute_volume(self):
        for record in self:
            if record.vehicle_category and record.vehicle_category.max_volume != 0:
                record.volume = record.volume / record.vehicle_category.max_volume
            else:
                record.volume = 0.0
                