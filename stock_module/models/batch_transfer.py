#-- coding: utf-8 --

from odoo import api, fields, models
from datetime import timedelta

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    vehicle = fields.Many2one(string="Vehicle", comodel_name="fleet.vehicle")
    vehicle_category = fields.Many2one(string="Category", comodel_name="fleet.vehicle.model.category")
    weight = fields.Float(string="Weight(kg)", compute="_compute_weight", default=0)
    volume = fields.Float(string="Volume", compute="_compute_volume", default=0)
    start_date = fields.Date(string="Start Date", compute="_compute_dates", store=True)
    end_date = fields.Date(string="End Date", compute="_compute_dates", store=True)
    dock_id = fields.Many2one(string="Dock id", comodel_name="stock.transport.dock")

    @api.depends("create_date")
    def _compute_dates(self):
            for record in self:
                start_date = record.scheduled_date

                end_date = fields.Datetime.from_string(start_date) + timedelta(days=7)

                record.start_date = start_date
                record.end_date = end_date

    @api.depends('vehicle_category.max_weight', 'weight')
    def _compute_weight(self):
        for record in self:
            max_weight = record.vehicle_category.max_weight
            record.weight = record.weight / max_weight if max_weight != 0 else 0.0

    @api.depends('vehicle_category.max_volume', 'volume')
    def _compute_volume(self):
        for record in self:
            max_volume = record.vehicle_category.max_volume
            record.volume = record.volume / max_volume if max_volume != 0 else 0.0

