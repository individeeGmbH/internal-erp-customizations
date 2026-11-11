import frappe
from frappe.utils import add_days, getdate

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

    def create_task_and_notify_user(self):
        # ERPNext refuses Tasks starting before the Project's expected_start_date,
        # and HRMS creates the Project with that set to date_of_joining. Pull the
        # Project start back to the earliest activity *before* inserting Tasks.
        self.set_project_start_date()
        super().create_task_and_notify_user()

    def set_project_start_date(self):
        if not self.project:
            return

        holiday_list = self.get_holiday_list()
        candidates = [
            getdate(self.get_task_dates(activity, holiday_list)[0])
            for activity in self.activities
            if activity.begin_on is not None
        ]

        current = frappe.db.get_value("Project", self.project, "expected_start_date")
        if current:
            candidates.append(getdate(current))

        expected_start = min(candidates) if candidates else getdate(self.date_of_joining)
        if not current or getdate(current) != expected_start:
            frappe.db.set_value(
                "Project",
                self.project,
                "expected_start_date",
                expected_start,
                update_modified=False,
            )
