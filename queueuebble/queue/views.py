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
      send_mail('Welcome to queueubble!', 'Thanks for registering.', 'jonathanp.chen@gmail.com', [user.email], fail_silently=False)
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
        if request.POST.get('next') != '/' and request.POST.get('next') != None:
          print request.POST.get('next')
          print "i'm here"
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
  exists = False
  queuename = None

  if request.method == 'POST':
    if 'createQueue' in request.POST:
      queuename = request.POST['queuename']
      queues = len(Queue.objects.filter(name=queuename, owner=puser))
      if queues == 0:
        queue = Queue(name=queuename, creator=puser)
        queue.save()
        queue.owner.add(puser)
        queue.save()
      else:
        exists = True
    if 'closeOpen' in request.POST:
      queueid = request.POST['queueid']
      queue_to_close = Queue.objects.get(id=queueid)
      queue_to_close.closed = not queue_to_close.closed
      queue_to_close.save()

  owned = Queue.objects.filter(owner=puser)
  favorites = puser.favorites.all()
  visited = puser.visited.all()
  qin = []
  for n in Node.objects.filter(user=puser):
    qin.append(n.queue)
  return render(request, 'queue/dashboard.html', locals())

def profile(request, username):
  u = User.objects.get(username=username)
  puser = UserProfile.objects.get(user=u)
  owned = Queue.objects.filter(owner=puser)

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
  myqueue = p in queue.owner.all()
  contains = queue.contains(p)
  users_nodes = Node.objects.filter(queue=queue, user=p)
  user_node = None
  fav = queue in p.favorites.all()
  if not len(users_nodes) == 0:
    user_node = users_nodes[0]

  if request.method == 'POST':
    if 'addFavorite' in request.POST:
      p.favorites.add(queue)
      fav = True
    if 'removeFavorite' in request.POST:
      p.favorites.remove(queue)
      fav = False
    if ('addMyself' in request.POST) and not queue.contains(p):
      node = Node(user=p, queue=queue, position=qsize)
      queue.size = qsize + 1
      queue.save()
      node.save()
      contains = True
      nodes = list(Node.objects.filter(queue=queue))
    if 'removeMyself' in request.POST:
      if not user_node == None:
        del_pos = user_node.position
        print del_pos
        user_node.delete()
        queue.size = queue.size - 1
        queue.save()
        nodes = list(Node.objects.filter(queue=queue))
        for n in nodes:
          if n.position > del_pos:
            n.position = n.position - 1
            n.save()
        nodes.sort(key=lambda x: x.position)
      contains = False
    if 'removeFromMyQueue' in request.POST:
      uRemoveName = request.POST.get('nodeToRemove2')
      if not uRemoveName == None:
        uRemoveUser = User.objects.get(username=uRemoveName)
        uRemoveProf = UserProfile.objects.get(user=uRemoveUser)
        uRemoveNodes = Node.objects.filter(queue=queue,user=uRemoveProf)
        if not len(uRemoveNodes) == 0:
          uRemoveNode = uRemoveNodes[0];
          uRemovePos = uRemoveNode.position
          uRemoveNode.delete();
          queue.size = queue.size - 1
          if queue.size>0:
            uNextUser = User.objects.get(username=uRemoveNodes[1])
            send_mail('Youre on deck!', 'Yo get ready', 'jonathanp.chen@gmail.com', [uNextUser.email], fail_silently=False)
          queue.save();
          nodes = list(Node.objects.filter(queue=queue))
          for n in nodes:
            if n.position > uRemovePos:
              n.position = n.position - 1
              n.save()
          nodes.sort(key=lambda x: x.position)
    if 'reorderQueue' in request.POST:
      ns = request.POST.get('reorderData').split(',')
      nodes = Node.objects.filter(queue=queue)
      i = 0
      for user_name in ns:
        user_object = User.objects.get(username=user_name)
        up_object = UserProfile.objects.get(user=user_object)
        no = nodes.get(user=up_object)
        no.position = i
        no.save()
        i = i + 1
    if 'changeStatus' in request.POST:
      userNameS = request.POST.get('statusChangeUser')
      if not userNameS == None:
        userS = User.objects.get(username=userNameS)
        userSProf = UserProfile.objects.get(user=userS)
        userSNodes = Node.objects.filter(queue=queue,user=userSProf)
        if not len(userSNodes) == 0:
          userSNode = userSNodes[0];
          userSNode.status = userSNode.status + 1;
          userSNode.save()
          nodes = list(Node.objects.filter(queue=queue))
          nodes.sort(key=lambda x: x.position)
    if 'addOwner' in request.POST:
      usernameO = request.POST.get('newowner')
      if User.objects.filter(username=usernameO):
        userO = User.objects.get(username=usernameO)
        userOProf = UserProfile.objects.get(user=userO)
        queue.owner.add(userOProf)
        queue.save()
    if 'openClose' in request.POST:
      queue.closed = not queue.closed
      queue.save()

  users_nodes = Node.objects.filter(queue=queue, user=p)
  owners = queue.owner.all()
  user_node = None
  if not len(users_nodes) == 0:
    user_node = users_nodes[0]
  return render(request, 'queue/queue.html', locals())

def search(request):
  if 'q' in request.GET and request.GET['q']:
    q = request.GET['q']
    queues = Queue.objects.filter(name__icontains=q)
    users = User.objects.filter(username__icontains=q)
    return render(request, 'queue/search_results.html', {'queues': queues, 'users': users, 'query': q})
  else:
    return HttpResponse('Submit a search term')
