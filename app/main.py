from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import HardwareForm, SoftwareForm
from .models import Hardware, Software, User # Assuming User might be needed for assigned_to
from . import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required # Redirect to login if not authenticated
def dashboard():
    # This could be the same as the existing 'index' route, or a more detailed dashboard
    # For now, let's assume it renders the main dashboard page
    return render_template('index.html', title='Dashboard') # Assuming index.html is the main dashboard

@main_bp.route('/hardware/add', methods=['GET', 'POST'])
@login_required
def add_hardware():
    form = HardwareForm()
    if form.validate_on_submit():
        new_hardware = Hardware(
            name=form.name.data,
            type=form.type.data,
            serial_number=form.serial_number.data if form.serial_number.data else None,
            purchase_date=form.purchase_date.data,
            warranty_expiry_date=form.warranty_expiry_date.data,
            location=form.location.data,
            status=form.status.data,
            description=form.description.data,
            # assigned_to_user_id could be added here if needed, e.g. from another form field
            # registration_date is handled by default in model
        )
        db.session.add(new_hardware)
        db.session.commit()
        flash(f'Hardware "{new_hardware.name}" added successfully!', 'success')
        return redirect(url_for('main.dashboard')) # Or redirect to an inventory list page
    return render_template('main/add_hardware.html', title='Add Hardware', form=form)

@main_bp.route('/software/add', methods=['GET', 'POST'])
@login_required
def add_software():
    form = SoftwareForm()
    if form.validate_on_submit():
        try:
            seats_val = int(form.seats.data) if form.seats.data else 1
        except ValueError:
            flash('Invalid value for Number of Seats. Must be a number.', 'danger')
            return render_template('main/add_software.html', title='Add Software', form=form)

        new_software = Software(
            name=form.name.data,
            version=form.version.data,
            license_key=form.license_key.data,
            purchase_date=form.purchase_date.data,
            expiry_date=form.expiry_date.data,
            seats=seats_val,
            installation_location=form.installation_location.data,
            supplier=form.supplier.data,
            description=form.description.data
            # registration_date is handled by default in model
        )
        db.session.add(new_software)
        db.session.commit()
        flash(f'Software "{new_software.name}" added successfully!', 'success')
        return redirect(url_for('main.dashboard')) # Or redirect to an inventory list page
    return render_template('main/add_software.html', title='Add Software', form=form)


@main_bp.route('/inventory')
@login_required
def view_inventory():
    hardware_items = Hardware.query.order_by(Hardware.registration_date.desc()).all()
    software_items = Software.query.order_by(Software.registration_date.desc()).all()
    return render_template('main/inventory.html', title='View Inventory',
                           hardware_items=hardware_items,
                           software_items=software_items)
