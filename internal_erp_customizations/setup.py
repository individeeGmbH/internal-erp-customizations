from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def setup_customizations():
    # Allow negative begin_on so activities can be scheduled before date_of_joining.
    make_property_setter(
        "Employee Boarding Activity",
        "begin_on",
        "non_negative",
        0,
        "Check",
        validate_fields_for_doctype=False,
    )
