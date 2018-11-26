from flask import url_for, flash, redirect


def csrf_validate(form):
    if not form.validate_on_submit():
        return False
    return True
