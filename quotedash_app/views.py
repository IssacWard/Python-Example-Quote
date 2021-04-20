from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    if 'user_id' not in request.session:
        return render(request, "index.html")
    else:
        return redirect('/quotes')


def register(request):
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        user = User.objects.filter(email=request.POST['email'])
        if user:
            messages.error(request, "Email is already in use.", extra_tags="email2")
            return redirect('/')

        pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()

        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw
        )

        request.session['user_id'] = User.objects.last().id
        return redirect('/quotes')

    else:
        return redirect('/')


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        user = User.objects.filter(email=request.POST['login_email'])
        if len(user) == 0:
            messages.error(request, "Invalid Email/Password", extra_tags="login")
            return redirect('/')

        if not bcrypt.checkpw(request.POST['login_password'].encode(), user[0].password.encode()):
            messages.error(request, "Invalid Email/Password", extra_tags="login")
            return redirect('/')

        request.session['user_id'] = user[0].id
        return redirect('/quotes')

    else:
        return redirect('/')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')

#-------------------------------------------#

def quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:

        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_quotes': Quote.objects.all(),
            'liked_quotes': Quote.objects.filter(liked_by=request.session['user_id']),
        }
        return render(request, "quotes.html", context)


def add_quote(request):
    if request.method == "POST":
        errors = Quote.objects.upload_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/quotes')
        Quote.objects.create(
            quote=request.POST['quote'],
            author=request.POST['author'],
            uploaded_by=User.objects.get(id=request.session['user_id'])
        )
        a = Quote.objects.last()
        b = User.objects.get(id=request.session['user_id'])
        a.liked_by.add(b)

        return redirect('/quotes')
    else:
        return redirect('/logout')


def delete_quote(request, id_from_route):
    remove = Quote.objects.get(id=id_from_route)
    remove.delete()
    return redirect('/quotes')


def like(request, id_from_route):
    a = Quote.objects.get(id=id_from_route)
    b = User.objects.get(id=request.session['user_id'])
    a.liked_by.add(b)
    return redirect('/quotes')


def unlike(request, id_from_route):
    a = Quote.objects.get(id=id_from_route)
    b = User.objects.get(id=request.session['user_id'])
    a.liked_by.remove(b)
    return redirect('/quotes')


def user(request, id_from_route):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_quotes': Quote.objects.all(),
            'user_page': User.objects.get(id=id_from_route),
            'liked_quotes': Quote.objects.filter(liked_by=request.session['user_id']), 
        }
        return render(request, "user.html", context)


def myaccount(request, id_from_route):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
        }
        return render(request, "myaccount.html", context)


def edit_user(request, id_from_route):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect(f'/myaccount/{id_from_route}')

        if User.objects.get(id=id_from_route).email == request.POST['edit_email']:
            pass
        else:
            user = User.objects.filter(email=request.POST['edit_email'])
            if user:
                    messages.error(request, "Email is already in use.", extra_tags="edit_email2")
                    return redirect(f'/myaccount/{id_from_route}')

        editable = User.objects.get(id=id_from_route)
        editable.first_name = request.POST['edit_first_name']
        editable.last_name = request.POST['edit_last_name']
        editable.email = request.POST['edit_email']
        editable.save()

        return redirect('/quotes')

    else:
        return redirect('/')
