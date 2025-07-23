from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash
from models import db, Store
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def root():
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['logged_in'] = True
            return redirect(url_for('admin.homepage'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@admin_bp.route('/homepage')
def homepage():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))
    stores = Store.query.all()
    return render_template('homepage.html', stores=stores)

@admin_bp.route('/add_store', methods=['POST'])
def add_store():
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))

    hashed_password = generate_password_hash(request.form['password'])
    new_store = Store(
        name=request.form['store_name'],
        postcode=request.form['postcode'],
        date=request.form['date'],
        owner=request.form['owner_name'],
        password=hashed_password,
        active=True
    )
    try:
        db.session.add(new_store)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return render_template('homepage.html', stores=Store.query.all(), error="Store name must be unique.")
    return redirect(url_for('admin.homepage'))

@admin_bp.route('/toggle_store/<store_id>', methods=['POST'])
def toggle_store(store_id):
    if not session.get('logged_in'):
        return redirect(url_for('admin.login'))
    store = Store.query.get(store_id)
    if store:
        store.active = not store.active
        db.session.commit()
    return redirect(url_for('admin.homepage'))
@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))
