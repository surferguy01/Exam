from django.shortcuts import render, redirect
from django.contrib import messages
from .models import*
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_password
        )
        request.session['user_id'] = new_user.id
        return redirect('/wishes')
    return redirect('/')


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/wishes')
    return redirect('/')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user' : this_user[0],  
        'all_wishes' : Wish.objects.all(),
        # 'granted_wishes' : Wish.objects.filter(granted = 'yes',)
    }
    return render(request, 'dashboard.html', context)


def new_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user' : this_user[0],  
    }
    return render(request, 'new_wish.html', context)


def create_wish(request):
    if 'user_id' not in request.session:
        return redirect('/')
    
    errors = Wish.objects.wish_validater(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wish/new')

    else:
        if request.method == "POST":
            this_user = User.objects.get(id = request.session['user_id'])

            Wish.objects.create(
                wish = request.POST['wish'],
                description = request.POST['description'],
                wish_maker = this_user)

    return redirect('/wishes')

# def granted_wish(request, wish_id):
#     if 'user_id' not in request.session:
#         return redirect('/')

#     wish = Wish.objects.get(id= wish_id)
#     wish.granted='yes'
#     wish.save()

#     return redirect('/wishes')


def edit(request, wish_id):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user = User.objects.filter(id = request.session['user_id'])
    this_wish = Wish.objects.get(id=wish_id)

    context = {
        'user' : this_user[0],
        'wish' : this_wish
    }
    return render(request, 'edit_wish.html', context)


def update(request, wish_id):
    if 'user_id' not in request.session:
        return redirect('/')

    update_wish = Wish.objects.get(id=wish_id)
    update_wish.wish = request.POST['title']
    update_wish.description = request.POST['description']
    update_wish.save()

    return redirect('/wishes')


# def like(request):
#     if 'user_id' not in request.session:
#         return redirect('/')
    
#     this_user = User.objects.filter(id = request.session['user_id'])
#     this_wish = Wish.objects.get(id=wish_id)


def wish(request):
    if 'user_id' not in request.session:
        return redirect('/')

    this_user = User.objects.filter(id = request.session['user_id'])
    # this_wish = Wish.objects.get(id=wish_id)

    context = {
        'user' : this_user[0],
        # 'this_wish' : this_wish
    }
    return render(request, 'wish.html', context)


def delete(request):
    if request.method == "POST":
        delete_wish = Wish.objects.get(id=request.POST['delete_wish'])
        delete_wish.delete()
    return redirect('/wishes')


def logout(request):
    request.session.flush()
    return redirect('/')