from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User, db
from app.models.workspace import Workspace
from app.forms import WorkspaceForm, UserWorkspaceForm

admin_bp = Blueprint('admin', __name__)

# Middleware za proveru admin privilegija
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Nemate pristup ovoj stranici.', 'danger')
            return redirect(url_for('shopping.list'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/admin/workspaces', methods=['GET', 'POST'])
@login_required
@admin_required
def workspaces():
    form = WorkspaceForm()
    if form.validate_on_submit():
        workspace = Workspace(name=form.name.data)
        db.session.add(workspace)
        db.session.commit()
        flash('Workspace je uspešno kreiran.', 'success')
        return redirect(url_for('admin.workspaces'))
    
    workspaces = Workspace.query.order_by(Workspace.name).all()
    return render_template('admin/workspaces.html', title='Workspace-ovi', workspaces=workspaces, form=form)

@admin_bp.route('/admin/workspace/<int:workspace_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_workspace(workspace_id):
    workspace = Workspace.query.get_or_404(workspace_id)
    
    # Provera da li workspace ima korisnike
    if workspace.users:
        flash('Ne možete obrisati workspace koji ima korisnike.', 'danger')
        return redirect(url_for('admin.workspaces'))
    
    db.session.delete(workspace)
    db.session.commit()
    flash('Workspace je uspešno obrisan.', 'success')
    
    return redirect(url_for('admin.workspaces'))

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    form = UserWorkspaceForm()
    # Popunjavamo opcije za dropdown liste
    form.user_id.choices = [(u.id, u.username) for u in User.query.order_by(User.username).all()]
    form.workspace_id.choices = [(w.id, w.name) for w in Workspace.query.order_by(Workspace.name).all()]
    
    if form.validate_on_submit():
        user = User.query.get_or_404(form.user_id.data)
        workspace = Workspace.query.get_or_404(form.workspace_id.data)
        
        user.workspace_id = workspace.id
        db.session.commit()
        flash(f'Korisnik {user.username} je uspešno dodeljen workspace-u {workspace.name}.', 'success')
        return redirect(url_for('admin.users'))
    
    users = User.query.order_by(User.username).all()
    return render_template('admin/users.html', title='Korisnici', users=users, form=form)

@admin_bp.route('/admin/user/<int:user_id>/admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    # Ne dozvoljavamo oduzimanje admin privilegija sebi
    if user.id == current_user.id:
        flash('Ne možete promeniti svoje admin privilegije.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = "dodeljen" if user.is_admin else "oduzet"
    flash(f'Korisniku {user.username} je {status} admin status.', 'success')
    
    return redirect(url_for('admin.users'))
