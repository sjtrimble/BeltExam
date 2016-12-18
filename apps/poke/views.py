from django.shortcuts import render, redirect
from models import User, Pokes
import bcrypt
from django.contrib import messages, sessions
from django.db.models import Count
from datetime import datetime

def index(request):
	if 'userid' not in request.session:
		return render(request, 'poke/index.html')
	else:
		return redirect('/pokes')

def registration(request):
	data = User.objects.registrationvalidation(request.POST)
	if data[0]:
		messages.success(request, "You have successfully logged in!")
		user = data[1]
		request.session['userid'] = user.id
		return redirect('/pokes')
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
		return redirect('/')
	else:
		errors = User.objects.loginvalidation(request.POST)[1]
		for error in errors:
			messages.error(request, error)
	return redirect('/')

def pokes(request):
	if 'userid' not in request.session:
		messages.error(request, "Please log in to view this page.")
		return redirect('/')
	userid = request.session['userid']
	loggedinuser = User.objects.filter(id=userid)[0]
	context = {
	"thisuser": loggedinuser,
	"users": User.objects.all().exclude(id=userid),
	"userpoked": Pokes.objects.filter(poked__id=userid), #where this user has been poked
	"allpokes": Pokes.objects.all(),
	# "allpokecounts": Pokes.objects.all().count(),
	"userpokedcount": Pokes.objects.filter(poked__id=userid).values('user').annotate(Count('user')).count()
	########## "allquotes": Quote.objects.all().exclude(favoritequote__user__id=userid).order_by('-created_at'),
	########## "favoritequotes": Favorite.objects.filter(user__id = userid)
	}
	return render (request, 'poke/pokes.html', context)

def pokeuser(request):
	userid = request.session['userid']
	if Pokes.objects.pokeauser(request.POST, userid):
		return redirect('/pokes')

def logout(request):
	for key in request.session.keys():
		del request.session[key]
		messages.success(request, "You have successfully logged out!")
	return redirect('/')