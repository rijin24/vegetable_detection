from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from models import db, Vegetable, Store
import os

store_bp = Blueprint('store', __name__)

@store_bp.route('/store_login', methods=['GET', 'POST'])
def store_login():
    if request.method == 'POST':
        store = Store.query.filter_by(name=request.form['store_name']).first()
        if store and check_password_hash(store.password, request.form['password']):
            session['store_id'] = store.id
            return redirect(url_for('store.store_dashboard'))
        return render_template('store_login.html', error="Invalid credentials")
    return render_template('store_login.html')

@store_bp.route('/store_dashboard', methods=['GET', 'POST'])
def store_dashboard():
    if 'store_id' not in session:
        return redirect(url_for('store.store_login'))
    store_id = session['store_id']

    if request.method == 'POST':
        for veg_id, new_stock in request.form.items():
            if veg_id.startswith('stock_'):
                veg_id_num = int(veg_id.split('_')[1])
                vegetable = Vegetable.query.filter_by(id=veg_id_num, store_id=store_id).first()
                if vegetable:
                    try:
                        vegetable.stock = int(new_stock)
                    except ValueError:
                        pass
        db.session.commit()
        return redirect(url_for('store.store_dashboard'))

    vegetables = Vegetable.query.filter_by(store_id=store_id).all()
    store = Store.query.get(store_id)
    return render_template('store_dashboard.html', vegetables=vegetables, store=store)

@store_bp.route('/add_vegetable', methods=['POST'])
def add_vegetable():
    if 'store_id' not in session:
        return redirect(url_for('store.store_login'))

    store_id = session['store_id']
    name = request.form['name'].strip().lower()  # Normalize for consistent matching

    # Check for duplicate vegetable for the same store
    existing_veg = Vegetable.query.filter_by(name=name, store_id=store_id).first()
    if existing_veg:
        store = Store.query.get(store_id)
        vegetables = Vegetable.query.filter_by(store_id=store_id).all()
        return render_template(
            'store_dashboard.html',
            vegetables=vegetables,
            store=store,
            error="Vegetable already exists for this store."
        )

    image = request.files.get('image')
    filename = None
    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image_path = os.path.join('static/uploads', filename)
        image.save(image_path)
    else:
        image_path = None

    try:
        new_veg = Vegetable(
            name=name,
            stock=int(request.form['stock']),
            image_path=image_path,
            store_id=store_id
        )
        db.session.add(new_veg)
        db.session.commit()
        success_message = "Vegetable added successfully."
    except Exception as e:
        db.session.rollback()
        success_message = "Failed to add vegetable."

    store = Store.query.get(store_id)
    vegetables = Vegetable.query.filter_by(store_id=store_id).all()
    return render_template(
        'store_dashboard.html',
        vegetables=vegetables,
        store=store,
        success=success_message
    )

@store_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('store.store_login'))
