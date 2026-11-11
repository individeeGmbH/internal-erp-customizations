import frappe


def set_project_start_date(doc, method=None):
    """HRMS creates the onboarding Project with ``expected_start_date`` set to
    ``date_of_joining`` (see ``EmployeeBoardingController.on_submit``). We run
    pre-joining onboarding tasks, so align the Project with
    ``boarding_begins_on`` instead. Task dates are already derived from
    ``boarding_begins_on`` by HRMS, so only the Project needs fixing.

    Registered as a ``doc_events`` hook on ``Employee Onboarding.on_submit``,
    which Frappe runs after the controller's own ``on_submit``, so
    ``doc.project`` is already set.
    """
    if not doc.project or not doc.boarding_begins_on:
        return

    frappe.db.set_value(
        "Project",
        doc.project,
        "expected_start_date",
        doc.boarding_begins_on,
        update_modified=False,
    )
