from queue.forms import UserForm, UserProfileForm
from queue.models import UserProfile, Queue, Node
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

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

      #send confirmation mail
      send_mail('Welcome to queueubble!', 'Sup niggs.', 'jonathanp.chen@gmail.com', [user.email], fail_silently=False)
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
        if request.POST.get('next') != '/':
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
  puser = UserProfile.objects.get(user=request.user)

  if request.method == 'POST':
    queuename = request.POST['queuename']
    queue = Queue(name=queuename)
    queue.save()
    queue.owner.add(puser)

  owned = Queue.objects.filter(owner=puser)
  qin = []
  for n in Node.objects.filter(user=puser):
    qin.append(n.queue)
  return render(request, 'queue/dashboard.html', locals())

def profile(request, username):
  u = User.objects.get(username=username)
  puser = UserProfile.objects.get(user=u)
  owned = Queue.objects.filter(owner=puser)

  print username
  return render(request, 'queue/profile.html', locals())

@login_required
def profile_id(request, username, uid):
  u = User.objects.get(username=username)
  puser = UserProfile.objects.get(user=u)
  queue = Queue.objects.get(owner=puser, id=uid)
  nodes = list(Node.objects.filter(queue=queue))
  nodes.sort(key=lambda x: x.position)
  qsize = queue.size
  p = UserProfile.objects.get(user=request.user)
  myqueue = p == puser
  contains = queue.contains(p)

  if request.method == 'POST' and not queue.contains(p):
    node = Node(user=p, queue=queue, position=qsize)
    queue.size = qsize + 1
    queue.save()
    node.save()
    contains = True
    print queue.size
    nodes = list(Node.objects.filter(queue=queue))

  users_nodes = Node.objects.filter(queue=queue, user=p)

  user_node = None
  if not len(users_nodes) == 0:
    user_node = users_nodes[0]

  return render(request, 'queue/queue.html', locals())
