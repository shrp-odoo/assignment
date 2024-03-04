#-- coding: utf-8 --
#Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Stock Transport",
    "category": "Stock Transport",
    "description": "This is for adding new features in fleet",
    "summary": "Transport management system",
    "installable": True,
    "application": True,
    "auto_install": True,
    "license": "OEEL-1",
    "version": "1.0",
    "depends": ["base", "fleet", "stock_picking_batch"],
    "data": [
        "views/fleet_vehicle_category_views.xml",
        "views/batch_transfer_category_views.xml",
        "views/batch_transfer_views.xml"
    ]
}
