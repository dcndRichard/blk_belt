from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *


def index(request):
    return render(request, 'index.html')

def process_register(request):
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    errors = User.objects.basic_validator(request.POST)

    if request.session.get('uid') is not None:
        return redirect('/quotes')

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')

    new_user= User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashed_pw,
        )

    request.session['uid'] = new_user.id
    request.session['first_name'] = new_user.first_name

    return redirect('/quotes')




def process_login(request):
    # first checks if user is logged in 
    if request.session.get('uid') is not None:
        return redirect('/quotes')

    found_user= User.objects.filter(email=request.POST['email'])
    if len(found_user) > 0:
        is_pw_correct = bcrypt.checkpw(request.POST['password'].encode(),
                                found_user.first().password.encode())
        if is_pw_correct is True:
            request.session['uid'] = found_user.first().id
            request.session['first_name'] = found_user.first().first_name
            return redirect('/quotes')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')
    else:
        messages.error(request,"Invalid credentials")
        return redirect('/quotes')





def quotes(request):
     # first checks if user is logged in 
    if request.session.get('uid') is None:
        return redirect('/')
    
    
    content={
        'user': User.objects.get(id=request.session.get('uid')),
        'quotes' : Quote.objects.all()
    }

    return render(request,'quotes.html',content)





def myaccount(request,acct_id):
     # first checks if user is logged in 
    if request.session.get('uid') is None:
        return redirect('/')

    content={
        'user': User.objects.get(id=request.session.get('uid'))
    }

    return render(request,'myaccount.html',content)




def process_edit_account(request):
    # first checks if user is logged in 
    if request.session.get('uid') is None:
        return redirect('/')

    errors = User.objects.acct_edit_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect(f"/myaccount/{request.session.get('uid')}")

    user_to_edit = User.objects.filter(id=request.session['uid'])
    if len(user_to_edit) > 0:
        user_to_edit = user_to_edit.first()
        user_to_edit.first_name = request.POST['first_name']
        user_to_edit.last_name = request.POST['last_name']
        user_to_edit.email = request.POST['email']
        user_to_edit.save()
        return redirect('/quotes')

    return redirect('/')




def process_quote_new(request):
    # check for errors
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/quotes")

    new_quote = Quote.objects.create(
        author=request.POST['author'],
        quote=request.POST['quote'],
        users_who_posted= User.objects.get(id=request.session['uid'])
       
    )

    return redirect('/quotes')





def process_quote_like(request,quote_id):
# redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')


    # finds wishes excluding user
    found_quote= Quote.objects.filter(id=quote_id).exclude(users_who_posted=request.session['uid'])
    loggin_user = User.objects.get(id=request.session['uid'])
    if len(found_quote) > 0:
        quote_to_like= found_quote[0]

        if loggin_user in quote_to_like.users_who_liked.all():
            quote_to_like.users_who_liked.remove(loggin_user)
        else:
            quote_to_like.users_who_liked.add(loggin_user)

    return redirect('/quotes')


def user(request,user_id):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')

    content = {
        'user_posted_quotes' : Quote.objects.filter(users_who_posted=user_id)
    }
    return render(request,"user.html", content)



def quote_delete(request,quote_id):
    # redirect back to login if not logged in
    if request.session.get('uid') is None:
        return redirect('/')

    quote_to_delete = Quote.objects.filter(id=quote_id)

    if len(quote_to_delete) > 0:
        quote_to_delete.first().delete()

    return redirect('/quotes')


def logout(request):
    request.session.clear()
    return redirect('/')