from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.shopping_item import ShoppingItem
from app.forms import ShoppingItemForm
from app.models.user import db

shopping_bp = Blueprint('shopping', __name__)

@shopping_bp.route('/', methods=['GET', 'POST'])
@shopping_bp.route('/shopping', methods=['GET', 'POST'])
@login_required
def list():
    # Ako korisnik nema dodeljen workspace
    if not current_user.workspace_id:
        flash('Nemate dodeljen workspace. Obratite se administratoru.', 'warning')
        return render_template('shopping/list.html', items=None, form=None)
    
    form = ShoppingItemForm()
    
    # Ako je forma validna pri submit-u, dodajemo novu stavku
    if form.validate_on_submit():
        item = ShoppingItem(
            name=form.name.data,
            workspace_id=current_user.workspace_id,
            added_by=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash('Stavka je uspešno dodata.', 'success')
        return redirect(url_for('shopping.list'))
    
    # Dohvatamo sve stavke za trenutni workspace
    items = ShoppingItem.query.filter_by(workspace_id=current_user.workspace_id).order_by(ShoppingItem.created_at.desc()).all()
    
    return render_template('shopping/list.html', form=form, items=items)

@shopping_bp.route('/shopping/toggle/<int:item_id>', methods=['POST'])
@login_required
def toggle(item_id):
    item = ShoppingItem.query.get_or_404(item_id)
    
    # Provera da li korisnik pripada istom workspace-u kao i stavka
    if item.workspace_id != current_user.workspace_id:
        flash('Nemate dozvolu za ovu akciju.', 'danger')
        return redirect(url_for('shopping.list'))
    
    # Promena statusa stavke
    item.purchased = not item.purchased
    db.session.commit()
    
    return redirect(url_for('shopping.list'))

@shopping_bp.route('/shopping/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit(item_id):
    item = ShoppingItem.query.get_or_404(item_id)
    
    # Provera da li korisnik pripada istom workspace-u kao i stavka
    if item.workspace_id != current_user.workspace_id:
        flash('Nemate dozvolu za ovu akciju.', 'danger')
        return redirect(url_for('shopping.list'))
    
    form = ShoppingItemForm(obj=item)
    
    if form.validate_on_submit():
        item.name = form.name.data
        db.session.commit()
        flash('Stavka je uspešno izmenjena.', 'success')
        return redirect(url_for('shopping.list'))
    
    return render_template('shopping/edit.html', form=form, item=item)

@shopping_bp.route('/shopping/delete/<int:item_id>', methods=['POST'])
@login_required
def delete(item_id):
    item = ShoppingItem.query.get_or_404(item_id)
    
    # Provera da li korisnik pripada istom workspace-u kao i stavka
    if item.workspace_id != current_user.workspace_id:
        flash('Nemate dozvolu za ovu akciju.', 'danger')
        return redirect(url_for('shopping.list'))
    
    db.session.delete(item)
    db.session.commit()
    flash('Stavka je uspešno obrisana.', 'success')
    
    return redirect(url_for('shopping.list'))
