#-- coding: utf-8 --

from odoo import fields, models, api

class FleetVehicleCategory(models.Model):
    _inherit = "fleet.vehicle.model.category"

    max_weight = fields.Float(string="Max Weight(kg)")
    max_volume = fields.Float(string="Max Volume(m3)")
    name = fields.Char(compute='_compute_display_name', store=True)

    _sql_constraints = [
        (
            "check_max_weight",
            "CHECK(max_weight > 0)",
            "Max Weight must be strictly Positive"
        ),
        (
            "check_max_volume",
            "CHECK(max_volume > 0)",
            "Max Volume must be strictly Positive"
        )
    ]

    @api.depends('name', 'max_weight', 'max_volume')
    def _compute_display_name(self):
        for record in self:
            name = record.name
            if record.max_weight:
                name += ' - Max Weight: %.2f kg' % record.max_weight
            if record.max_volume:
                name += ' - Max Volume: %.2f m3' % record.max_volume
            record.display_name = name
