from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.musicians import Musician
from flask_app.models.users import User

@app.route('/musician/new')
def display_new():
    if not "user_id" in session:
        return redirect('/')
    return render_template('musician_new.html')

@app.route("/musician/create", methods=["POST"])
def create():
    if not "user_id" in session:
        return redirect('/')
    if not Musician.validator(request.form):
        return redirect('/musician/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    Musician.save(data)
    return redirect('/dashboard')

@app.route('/musician/edit/<int:id>')
def edit_display(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    musician = Musician.get_by_id(data)
    return render_template('musician_edit.html', musician=musician)

@app.route('/musician/update/<int:id>', methods=["POST"])
def update(id):
    if not "user_id" in session:
        return redirect('/')
    if not Musician.validator(request.form):
        return redirect(f'/musician/edit/{id}')
    data = {
        **request.form,
        'id': id
    }
    Musician.update(data)
    return redirect('/dashboard')

@app.route('/musician/destroy/<int:id>')
def destory(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id 
    }
    to_be_deleted = Musician.get_by_id(data)
    if not session['user_id'] == to_be_deleted.user_id:
        flash("Quit trying to delete other people's favorite artists", "err_destroy")
        return redirect('/')
    Musician.destroy(data)
    return redirect('/dashboard')

@app.route('/musicians/<int:id>')
def show_one(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    data2 = {
        'id': session['user_id']
    }
    musician = Musician.get_by_id(data)
    user = User.get_one_user(data2)
    return render_template("musician_view.html", musician=musician, user=user)

@app.route('/my_musicians')
def my_musicians():
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('my_musicians.html', user=user)

@app.route('/musicians/favorite/<int:id>')
def musician_favorites(id):
    if not "user_id" in session:
        return redirect('/')
    data = {
        'id': id
    }
    user = User.get_by_id(data)
    return render_template('musician_fave.html', user=user)