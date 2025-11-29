"""Flask web application for warehouse management."""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# In-memory storage for warehouses (name -> Varasto instance)
warehouses = {}


@app.route('/')
def index():
    """Main page showing all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/add', methods=['POST'])
def add_warehouse():
    """Add a new warehouse."""
    name = request.form.get('name', '').strip()
    try:
        tilavuus = float(request.form.get('tilavuus', 0))
        alku_saldo = float(request.form.get('alku_saldo', 0))
    except ValueError:
        flash('Invalid capacity or initial balance values!', 'error')
        return redirect(url_for('index'))

    if not name:
        flash('Warehouse name is required!', 'error')
        return redirect(url_for('index'))

    if name in warehouses:
        flash(f'Warehouse "{name}" already exists!', 'error')
        return redirect(url_for('index'))

    if tilavuus <= 0:
        flash('Capacity must be greater than 0!', 'error')
        return redirect(url_for('index'))

    warehouses[name] = Varasto(tilavuus, alku_saldo)
    flash(f'Warehouse "{name}" created successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/edit/<name>', methods=['POST'])
def edit_warehouse(name):
    """Edit an existing warehouse's capacity."""
    if name not in warehouses:
        flash(f'Warehouse "{name}" not found!', 'error')
        return redirect(url_for('index'))

    try:
        new_tilavuus = float(request.form.get('tilavuus', 0))
    except ValueError:
        flash('Invalid capacity value!', 'error')
        return redirect(url_for('index'))

    if new_tilavuus <= 0:
        flash('Capacity must be greater than 0!', 'error')
        return redirect(url_for('index'))

    old_varasto = warehouses[name]
    # Create new warehouse with updated capacity, keeping current balance
    new_saldo = min(old_varasto.saldo, new_tilavuus)
    warehouses[name] = Varasto(new_tilavuus, new_saldo)
    flash(f'Warehouse "{name}" updated successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<name>', methods=['POST'])
def delete_warehouse(name):
    """Delete a warehouse."""
    if name not in warehouses:
        flash(f'Warehouse "{name}" not found!', 'error')
        return redirect(url_for('index'))

    del warehouses[name]
    flash(f'Warehouse "{name}" deleted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/add_content/<name>', methods=['POST'])
def add_content(name):
    """Add content to a warehouse."""
    if name not in warehouses:
        flash(f'Warehouse "{name}" not found!', 'error')
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        flash('Invalid amount value!', 'error')
        return redirect(url_for('index'))

    if amount <= 0:
        flash('Amount must be greater than 0!', 'error')
        return redirect(url_for('index'))

    warehouses[name].lisaa_varastoon(amount)
    flash(f'Added {amount} to warehouse "{name}"!', 'success')
    return redirect(url_for('index'))


@app.route('/remove_content/<name>', methods=['POST'])
def remove_content(name):
    """Remove content from a warehouse."""
    if name not in warehouses:
        flash(f'Warehouse "{name}" not found!', 'error')
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
    except ValueError:
        flash('Invalid amount value!', 'error')
        return redirect(url_for('index'))

    if amount <= 0:
        flash('Amount must be greater than 0!', 'error')
        return redirect(url_for('index'))

    taken = warehouses[name].ota_varastosta(amount)
    flash(f'Removed {taken} from warehouse "{name}"!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
