app_name = "internal_erp_customizations"
app_title = "Internal ERP Customizations"
app_publisher = "Internal ERP"
app_description = "Customizations for the internal ERP"
app_email = "erp@individee.com"
app_license = "mit"

required_apps = ["frappe/erpnext", "frappe/hrms"]

override_doctype_class = {
    "Employee Onboarding": "internal_erp_customizations.overrides.employee_onboarding.CustomEmployeeOnboarding",
}

after_install = "internal_erp_customizations.setup.setup_customizations"
after_migrate = "internal_erp_customizations.setup.setup_customizations"