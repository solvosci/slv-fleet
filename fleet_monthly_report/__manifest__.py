# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Fleet Monthly Report",
    "summary": "Adds monthly report for each driver. ",
    "version": "17.0.1.0.0",
    "author": "Solvos",
    "category": "fleet",
    "license": "LGPL-3",
    "website": "https://github.com/solvosci/slv-fleet",
    "depends": [
        "fleet",
        "fleet_odometer_unit_count"
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/fleet_monthly_report_wizard_view.xml",
        "views/fleet_monthly_report_menu.xml",
        "reports/fleet_monthly_report.xml",
        "reports/fleet_monthly_template.xml",
    ],
}
