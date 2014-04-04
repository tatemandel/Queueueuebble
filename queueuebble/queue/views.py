from queue.forms import UserForm, UserProfileForm
from queue.models import UserProfile, Queue, Node
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

      pu = UserProfile(user=user)
      pu.save()
  
      profile = profile_form.save(commit=False)
      profile.user = user
      new_user = authenticate(username=request.POST['username'], \
                              password=request.POST['password'])
      new_user.backend='django.contrib.auth.backends.ModelBackend' 
      login(request, new_user)
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
        
        if request.POST.get('next') != '':
          print request.POST.get('next')
          return HttpResponseRedirect(request.POST.get('next'))
        else:
          return HttpResponseRedirect('/dashboard/')
      else:
        return HttpResponse("Your Queuebble account is disabled.")
    else:
      print "Invalid login details: {0}, {1}".format(username, password)
      return HttpResponse("Invalid login details supplied.")

  else:
    print request.GET.get('next', '/')
    context['next'] = request.GET.get('next', '/')
    return render_to_response('queue/login.html', {}, context)

def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')

@login_required
def dashboard(request):
  context = RequestContext(request)
  puser = UserProfile.objects.filter(user=request.user)
  owned = Queue.objects.filter(owner=puser)
  qin = []
  for n in Node.objects.filter(user=puser):
    qin.append(n.queue)

  return render(request, 'queue/dashboard.html', locals())
