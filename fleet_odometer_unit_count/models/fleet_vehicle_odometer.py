# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class FleetVehicleOdometer(models.Model):
    _inherit="fleet.vehicle.odometer"

    start = fields.Float(copy=False)
    difference = fields.Float(compute="_compute_difference")

    @api.constrains('start', 'value')
    def _check_start_not_higher_than_value(self):
        for record in self.filtered(lambda r: r.start and r.value):
            if record.value < record.start:
                unit = dict(record.vehicle_id._fields['odometer_unit'].selection).get(record.vehicle_id.odometer_unit)
                raise ValidationError(_(
                    "Final %(unit_display_name)s can't be lower than the initial %(unit_display_name)s",
                    unit_display_name=unit
                ))

    @api.constrains('start', 'value', 'date', 'vehicle_id')
    def _check_odometer_continuity(self):
        for record in self:
            if not record.start or not record.value or not record.date or not record.vehicle_id:
                continue

            all_odometers = self.search([
                ('vehicle_id', '=', record.vehicle_id.id),
                ('id', '!=', record.id)
            ]).sorted(key=lambda r: (r.date, r.start))

            same_day = all_odometers.filtered(lambda r: r.date == record.date)
            for od in same_day:
                if not (record.value <= od.start or record.start >= od.value):
                    raise ValidationError(_(
                        "Odometer range %(start)s-%(end)s overlaps with existing record "
                        "%(od_start)s-%(od_end)s for vehicle %(vehicle)s on %(date)s.",
                        start=record.start,
                        end=record.value,
                        od_start=od.start,
                        od_end=od.value,
                        vehicle=record.vehicle_id.name,
                        date=record.date
                    ))

            prev_od = all_odometers.filtered(lambda r: (r.date < record.date) or (r.date == record.date and r.value <= record.start))
            prev_od = prev_od.sorted(key=lambda r: (r.date, r.value), reverse=True)
            next_od = all_odometers.filtered(lambda r: (r.date > record.date) or (r.date == record.date and r.start >= record.value))
            next_od = next_od.sorted(key=lambda r: (r.date, r.start))

            if prev_od and record.start < prev_od[0].value:
                raise ValidationError(_(
                    "Odometer range %(start)s-%(end)s overlaps with previous record "
                    "%(od_start)s-%(od_end)s for vehicle %(vehicle)s on %(date)s.",
                    start=record.start,
                    end=record.value,
                    od_start=prev_od[0].start,
                    od_end=prev_od[0].value,
                    vehicle=record.vehicle_id.name,
                    date=prev_od[0].date
                ))

            if next_od and record.value > next_od[0].start:
                raise ValidationError(_(
                    "Odometer range %(start)s-%(end)s overlaps with next record "
                    "%(od_start)s-%(od_end)s for vehicle %(vehicle)s on %(date)s.",
                    start=record.start,
                    end=record.value,
                    od_start=next_od[0].start,
                    od_end=next_od[0].value,
                    vehicle=record.vehicle_id.name,
                    date=next_od[0].date
                ))

    @api.depends('value', 'start')
    def _compute_difference(self):
        for record in self:
            record.difference = record.value - record.start if record.value else 0.0
