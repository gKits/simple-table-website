from flask import request, redirect  # , render_template


def index():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass
    else:
        return redirect('/')


def create():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass
    else:
        return redirect('/')


def edit(id):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass
    else:
        return redirect('/')
