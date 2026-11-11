app_name = "internal_erp_customizations"
app_title = "Internal ERP Customizations"
app_publisher = "Internal ERP"
app_description = "Customizations for the internal ERP"
app_email = "erp@individee.com"
app_license = "mit"

required_apps = ["frappe/erpnext", "frappe/hrms"]

doc_events = {
    "Employee Onboarding": {
        "on_submit": "internal_erp_customizations.overrides.employee_onboarding.set_project_start_date",
    },
}
