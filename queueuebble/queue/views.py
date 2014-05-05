import json
from queue.forms import UserForm, UserProfileForm
from queue.models import UserProfile, Queue, Node
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import resolve
from django.views.decorators.csrf import csrf_exempt
 
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
      return HttpResponseRedirect('/')
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
    if 'destroy' in request.POST:
      queueid = request.POST['queueid']
      queue_to_destroy = Queue.objects.get(id=queueid)
      queue_to_destroy.delete()

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

def confirm_reorder(request, queue):
  arr = request.POST.getlist('arr[]')
  nodes = Node.objects.filter(queue=queue)
  i = 0
  for user_name in arr:
    user_object = User.objects.get(username=user_name)
    up_object = UserProfile.objects.get(user=user_object)
    no = nodes.get(user=up_object)
    no.position = i
    no.save()
    i = i + 1

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

    # ajax
    if request.POST.get('name') == "reorderQueue":
      confirm_reorder(request, queue)
      response = {'response' : "Order updated successfully!"}
      print response
      return HttpResponse(json.dumps(response), content_type="application/json")

    # not ajax
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
    if 'destroy' in request.POST:
      queue.delete()
      return HttpResponseRedirect('/dashboard/')

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

@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {
        'title': _('Password reset successful'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)
def pebble_login(request):
  return render_to_response('queue/pebble_login.html')

@csrf_exempt
def pebble_validate(request):
  if request.method == 'POST':
    arr = request.POST.getlist('arr[]')
    username = arr[0]
    password = arr[1]
    user = authenticate(username=username, password=password)

    if user is not None:
      return HttpResponse(username, status=200)
    return HttpResponse("Error", status=400)

@csrf_exempt
def pebble_get_admin(request):
  if request.method == 'POST':
    username = request.POST['username']
    user = User.objects.get(username=username)
    if user is not None:
      puser = UserProfile.objects.get(user=user)
      data = []
      for q in Queue.objects.filter(owner=puser):
        d = { 'name' : q.name,
              'id' : q.id,
              'size' : q.size,
              'status' : q.closed }
        data.append(d)
      return HttpResponse(json.dumps(data), content_type="application/json")
    else:
      return HttpResponse("Invalid username", status=400)
  else:
    return HttpResponse("Nothing to get", status=400)

@csrf_exempt
def pebble_get_member(request):
  if request.method == 'POST':
    username = request.POST['username']
    user = User.objects.get(username=username)
    if user is not None:
      puser = UserProfile.objects.get(user=user)
      data = []
      for n in Node.objects.filter(user=puser):
        d = { 'name' : n.queue.name,
              'creator' : n.queue.creator.user.username,
              'position' : n.position,
              'status' : n.queue.closed,
              'id' : n.queue.id }
        data.append(d)
      return HttpResponse(json.dumps(data), content_type="application/json")
    else:
      return HttpResponse("Invalid username", status=400)
  else:
    return HttpResponse("Nothing to get", status=400)

