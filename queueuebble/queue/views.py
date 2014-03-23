from queue.forms import UserForm, UserProfileForm
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
  return render(request, 'queue/index.html', {})

def register(request):
  context = RequestContext(request)
  registered = False

  if request.method == 'POST':
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileForm(data=request.POST)
    
    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()

      user.set_password(user.password)
      user.save()
  
      profile = profile_form.save(commit=False)
      profile.user = user
      registered = True
    else:
      print user_form.errors, profile_form.errors

  else:
    user_form = UserForm()
    profile_form = UserProfileForm()

  return render_to_response(
    'queue/register.html',
    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
    context)    

def user_login(request):
  context = RequestContext(request)
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    
    if user is not None:
      if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/')
      else:
        return HttpResponse("Your Queuebble account is disabled.")
    else:
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponse("Invalid login details supplied.")

  else:
    return render_to_response('queue/login.html', {}, context)

@login_required
def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')
