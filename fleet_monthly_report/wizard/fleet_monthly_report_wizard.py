# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, _, api
from odoo.exceptions import ValidationError
from datetime import datetime
import calendar


class FleetMonthlyReport(models.TransientModel):
    _name = "fleet.monthly.report.wizard"
    _description = "fleet.monthly.report.wizard"

    partner_ids = fields.Many2many('res.partner')
    odometer_ids = fields.Many2many('fleet.vehicle.odometer', compute='_compute_odometer_ids', store=True)
    month=fields.Selection(
                    [(str(i), _(month)) for i, month in enumerate(calendar.month_name) if month],
                    required=True, 
                    default=lambda self: str(datetime.today().month)
                )
    year=fields.Integer(
                    required=True, 
                    default=lambda self: str(datetime.today().year),
                    help="Enter a year in the format 19xx or 20xx."
                )

    @api.depends('partner_ids', 'month', 'year')
    def _compute_odometer_ids(self):
        for record in self:
            if record.month and record.year:
                selected_month = int(record.month)
                start_date = fields.Date.from_string(f'{record.year}-{selected_month:02d}-01')
                if selected_month < 12:
                    end_date = fields.Date.from_string(f'{record.year}-{selected_month + 1:02d}-01')
                else:
                    end_date = fields.Date.from_string(f'{record.year + 1}-01-01')
                
                domain = [('date', '>=', start_date),
                        ('date', '<', end_date)]
                if record.partner_ids:
                    domain += [('driver_id', 'in', record.partner_ids.ids)]

                record.odometer_ids = self.env['fleet.vehicle.odometer'].search(domain)
            else:
                record.odometer_ids = False

    @api.constrains('year')
    def _check_year_format(self):
        for record in self:
            if not (1900 <= record.year <= 2099):
                raise ValidationError(_("The year must be between 1900 and 2099."))

    def action_fleet_monthly_report(self):
        return self.env.ref('fleet_monthly_report.action_fleet_monthly_report').report_action(self)
