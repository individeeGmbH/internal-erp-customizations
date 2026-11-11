import frappe
from frappe.utils import add_days

from hrms.hr.doctype.employee_onboarding.employee_onboarding import EmployeeOnboarding


class CustomEmployeeOnboarding(EmployeeOnboarding):
    """Schedule onboarding activities relative to the joining date.

    HRMS computes task dates from ``boarding_begins_on`` and forbids negative
    ``begin_on`` values. We want ``begin_on`` to be an offset (possibly negative,
    for pre-joining work) from ``date_of_joining``. The ``non_negative`` flag is
    lifted via a Property Setter in ``internal_erp_customizations.setup``.
    """

    def get_task_dates(self, activity, holiday_list):
        start_date = end_date = None

        if activity.begin_on is not None:
            start_date = add_days(self.date_of_joining, activity.begin_on)
            start_date = self.update_if_holiday(start_date, holiday_list)

            if activity.duration is not None:
                end_date = add_days(self.date_of_joining, activity.begin_on + activity.duration)
                end_date = self.update_if_holiday(end_date, holiday_list)

        return [start_date, end_date]

    def on_submit(self):
        super().on_submit()
        self.set_project_start_date()

    def on_update_after_submit(self):
        super().on_update_after_submit()
        self.set_project_start_date()

    def set_project_start_date(self):
        """HRMS sets the Project's expected_start_date to date_of_joining; with
        pre-joining tasks the Project should start at the earliest task instead."""
        if not self.project:
            return

        task_starts = frappe.get_all(
            "Task",
            filters={"project": self.project, "exp_start_date": ("is", "set")},
            pluck="exp_start_date",
        )
        expected_start = min(task_starts) if task_starts else self.date_of_joining

        frappe.db.set_value(
            "Project",
            self.project,
            "expected_start_date",
            expected_start,
            update_modified=False,
        )
