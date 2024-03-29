#-- coding: utf-8 --

from odoo import api, fields, models
from datetime import timedelta

class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    vehicle = fields.Many2one(string="Vehicle", comodel_name="fleet.vehicle")
    vehicle_category = fields.Many2one(string="Category", comodel_name="fleet.vehicle.model.category")
    weight = fields.Float(string="Weight (kg)", compute="_compute_weight", store=True)
    volume = fields.Float(string="Volume (m3)", compute="_compute_volume", store=True)
    start_date = fields.Date(string="Start Date", compute="_compute_start_end_date", store=True)
    end_date = fields.Date(string="End Date", compute="_compute_start_end_date", store=True)
    dock_id = fields.Many2one(string="Dock id", comodel_name="stock.transport.dock")
    transfers_ids = fields.Float(string="Transfers", compute="_compute_transfer", store=True)
    lines_ids = fields.Float(string="Lines", compute="_compute_lines", store=True)
    total_weight = fields.Float(compute='_compute_total_weight', store=True)
    total_volume = fields.Float(compute='_compute_total_volume', store=True)

    @api.depends("create_date")
    def _compute_start_end_date(self):
            for record in self:
                start_date = record.scheduled_date
                end_date = fields.Datetime.from_string(start_date) + timedelta(hours=24)
                record.start_date = start_date
                record.end_date = end_date
                
    @api.depends('move_line_ids', 'vehicle_category')
    def _compute_total_weight(self):
        for record in self:
            total_weight = 0.0
            for line in record.move_line_ids:
                if line.product_id and line.product_id.weight:
                    total_weight += line.product_id.weight
            record.total_weight = total_weight

    @api.depends('total_weight', 'vehicle_category')
    def _compute_weight(self):
        for record in self:
            max_weight = record.vehicle_category.max_weight or 1.0
            record.weight = (record.total_weight / max_weight) * 100
    
    @api.depends('move_line_ids', 'vehicle_category')
    def _compute_total_volume(self):
        for record in self:
            total_volume = 0.0
            for line in record.move_line_ids:
                if line.product_id and line.product_id.volume:
                    total_volume = total_volume + line.product_id.volume
            record.total_volume = total_volume
           
    @api.depends('total_volume', 'vehicle_category')
    def _compute_volume(self):
        for record in self:
            max_volume = record.vehicle_category.max_volume or 1.0
            record.volume = (record.total_volume / max_volume) * 100

    @api.depends('vehicle_category')
    def _compute_display_name(self):
        for record in self:
            name = record.name 
            name += f"{record.vehicle_category.max_weight}kg  {record.vehicle_category.max_volume}m3  {record.vehicle.driver_id.name}"
            record.display_name = name

    @api.depends('picking_ids')
    def _compute_lines(self):
        for record in self:
            total_length = len(record.picking_ids)
            record.lines_ids = total_length

    @api.depends('move_line_ids')
    def _compute_transfer(self):
        for record in self:
            total_length = len(record.move_line_ids)
            record.transfers_ids = total_length
