from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.db import transaction
from models import *
import json
from django.core.urlresolvers import reverse


# Create your views here.
def get_all_users():
    return UserDetail.objects.all()
def home_page(request):
    final_list = {}
    users = get_all_users()
    final_list.update({'users': users})
    return render_to_response(
            'library/homepage.html',
            final_list
    )


@csrf_exempt
@transaction.atomic
def adduser(request):
    save_point = transaction.savepoint()
    response_dict = {}
    final_list = {'error': ''}
    if request.method == 'POST':
        try:
            UserDetail.objects.get(email__iexact=request.POST['email'])
            final_list['error'] = 'Email id Already Exist'
            transaction.savepoint_rollback(save_point)
        except UserDetail.DoesNotExist:
            user_id = str(uuid.uuid4()).split('-')[0]
            userdetail = UserDetail()
            userdetail.name = request.POST['name']
            userdetail.user_id = user_id
            userdetail.email = request.POST['email']
            userdetail.save()
    return HttpResponseRedirect('/lib')


@csrf_exempt
@transaction.atomic
def addbook(request):
    save_point = transaction.savepoint()
    if request.method == 'POST':
        try:
            Books.objects.get(name__iexact=request.POST['bookname'])
            print "here in book"
            final_list['error'] = 'Book Already Exist'
            transaction.savepoint_rollback(save_point)
        except Books.DoesNotExist:
            print "here book error"
            book = Books()
            book.name = request.POST['bookname']
            book.author = request.POST['authname']
            book.save()
    return HttpResponseRedirect('/lib')


@transaction.atomic
@csrf_exempt
def deleteuser(request):
    save_point = transaction.savepoint()
    response_dict = {}
    if request.method == 'POST':
        try:
            user_id = str(request.POST['id'])
            user = UserDetail.objects.get(user_id=user_id)
            user.delete()
            response_dict.update({'message': "success"})
        except UserDetail.DoesNotExist:
            transaction.savepoint_rollback(save_point)
            response_dict.update({'message': "error"})
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


@csrf_exempt
@transaction.atomic
def issuebook(request):
    save_point = transaction.savepoint()
    books = Books.objects.all()
    users = UserDetail.objects.all()
    return render_to_response(
            'library/issuebooks.html',
            {
                'books': books,
                'users': users
            }
    )


@csrf_exempt
@transaction.atomic
def issue(request):
    save_point = transaction.savepoint()
    if request.method == 'POST':
        try:
            book = Books.objects.get(pk=int(request.POST['selectbook']))
            user = UserDetail.objects.get(pk=int(request.POST['selectuser']))
            user_books = user.books.all()
            if not book in user_books:
                user.books.add(book)
                user.save()
                print "sucess"
            else:
                print "error"
        except:
            print "except"
    return HttpResponseRedirect('/lib')
