from django.shortcuts import render, HttpResponse, redirect
from.models import *
from django.contrib import messages
from datetime import datetime
import bcrypt
from ..app_one.models import *

# Create your views here.

def main(request):
    current_user = User.objects.get(id=request.session['user_id'])
    all_items = Item.objects.all().exclude(user_wish=request.session['user_id']).exclude(created_by = request.session['user_id'])
    my_items = Item.objects.filter(created_by = current_user)
    
    context = {
        'user_name' : current_user.fname,
        'all_items' : all_items,
        'my_items' : my_items,
        'items_joined' : Item.objects.filter(user_wish=request.session['user_id']),
        

    }
    return render(request,'wish_app/index.html',context)


def add(request):
    context = {}
    return render(request,'wish_app/add.html', context)

def processadd(request):
    if request.method == 'POST':
        errors = Item.objects.item_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wish/processadd')

        current_user = User.objects.get(id = request.session['user_id'])
        item = Item.objects.create(title = request.POST['title'],created_by = current_user)
        return redirect('/wish')

    elif request.method == 'GET':
        return render(request, 'wish_app/add.html')

def delete(request, id):
    user = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('/wish')

def cancel(request, id):
    userjoined = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=id)
    item.user_wish.remove(userjoined)
    item.save()
    return redirect('/wish')

def show(request, id):
    item = Item.objects.get(id=id)
    all_items = User.objects.filter(user_title = id)
    context = {
        'this_item' : item,
        'wish_item' : Item.objects.filter(id=request.session['user_id']),
        'all_item' : all_items.exclude(id=item.created_by.id)
    }
    return render(request, 'wish_app/show.html', context)

def join(request,id):
    if 'user_id' not in request.session:
        return redirect('/wish')
    item = Item.objects.get(id=id)
    userjoined = User.objects.get(id=request.session['user_id'])
    itemjoined = item.user_wish.add(userjoined)
    item.save()
    return redirect('/wish')

