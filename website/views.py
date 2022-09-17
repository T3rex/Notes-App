from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required    
from website.models import User, Note
from website import db

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method=="POST":
        note = request.form.get('note')
        
        new_note = Note(text=note,user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("New Note added", category="success")        

    return render_template("home.html", user=current_user)

@views.route('/delete/<noteId>')
def deleteNote(noteId): 
    note = Note.query.get(noteId)    
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit() 
            flash('Note deleted', category="success")
    return render_template("home.html", user=current_user)
