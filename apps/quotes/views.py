from django.shortcuts import render, redirect
from models import User, Quote, Favorite
import bcrypt
from django.contrib import messages, sessions
from django.db.models import Count

def index(request):
	if 'userid' not in request.session:
		return render(request, 'quotes/index.html')
	else:
		return redirect('/quotes')

def registration(request):
	data = User.objects.registrationvalidation(request.POST)
	if data[0]:
		messages.success(request, "You have successfully logged in!")
		user = data[1]
		request.session['userid'] = user.id
		return redirect('/quotes')
	else:
		errors = User.objects.registrationvalidation(request.POST)[1]
		for error in errors:
			messages.error(request, error)
		return redirect('/')

def login(request):
	if User.objects.loginvalidation(request.POST)[0]:
		messages.success(request, "You have successfully logged in!")
		user = User.objects.loginvalidation(request.POST)[1]
		print user
		request.session['userid'] = user.id
		print user.id
		return redirect('/quotes')
	else:
		errors = User.objects.loginvalidation(request.POST)[1]
		for error in errors:
			messages.error(request, error)
	return redirect('/')

def quotes(request):
	# if 'userid' not in request.session:
	# 	messages.error(request, "Please log in to view this page.")
	# 	return redirect('/')
	userid = request.session['userid']
	context = {
	"allquotes": Quote.objects.all().order_by('-created_at'),
	"user": User.objects.filter(id=userid)[0],
	# "favoritequotes": Favorite.objects.filter(user__id = userid)
	}
	return render (request, 'quotes/quotes.html', context)

def addquote(request):
	userid = request.session['userid']
	validquote = Quote.objects.quotevalid(request.POST, userid)
	if validquote[0]:
		return redirect('/quotes')
	else:
		for error in validquote[1]:
			messages.error(request, error)
			return redirect('/quotes')

def addtofavorites(request):
	userid = request.session['userid']
	quoteid = request.POST['quoteid']
	if Favorite.objects.addtofavorites(request.POST, userid, quoteid):
		return redirect('/quotes')

def removefavorite(request):
	quoteid = request.POST['quoteid']
	if Favorite.objects.removefavorite(request.POST, quoteid):
		return redirect('/quotes')

def user(request, id):
	user = User.objects.filter(id=id)[0]
	quotes = Quote.objects.filter(user__id=id)
	quotesnum = quotes.count()
	context = {
	"user": user,
	"quotes": quotes,
	"quotesnum": quotesnum
	}
	return render(request, 'quotes/user.html', context)

def logout(request):
	for key in request.session.keys():
		del request.session[key]
		messages.success(request, "You have successfully logged out!")
	return redirect('/')