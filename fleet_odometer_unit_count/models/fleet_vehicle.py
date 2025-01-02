# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, _
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    def write(self, vals_list):
        if 'driver_id' in vals_list:
            for vehicle in self:
                if vals_list['driver_id'] != vehicle.driver_id.id:
                    has_odometer_history = self.env['fleet.vehicle.odometer'].search_count([
                        ('vehicle_id', '=', vehicle.id)
                    ])
                    if has_odometer_history:
                        raise ValidationError(_(
                            "You cannot change the driver of a vehicle with odometer history."
                        ))
        return super().write(vals_list)
