from django.http import *
from django.shortcuts import render_to_response
from pitSimulator.PitSimulator.models import *
from pitSimulator.PitSimulator.forms import *

DELIMETER = "<||>"

def hello(request):
  return HttpResponse("Hello world. You are logged in as user '%s'" % request.COOKIES['user_id'])

def intro(request):
  if 'user_id' in request.COOKIES:
    try:
      user = User.objects.get(id = int(request.COOKIES['user_id']))
    except User.DoesNotExist:
      status = "Error: User with id %s does not exist" % request.COOKIES['user_id']
    else:
      teams = Team.objects.all()
      return render_to_response('home.html', locals())
  if len(Team.objects.all()) == 0:
    return HttpResponseRedirect('/teams/register/')
  elif len(User.objects.all()) == 0:
    return HttpResponseRedirect('/users/register/')
  else:
    return HttpResponseRedirect('/users/login/')

def displayMeta(request):
  values = request.META.items()
  values.sort()
  return render_to_response("metaInfo.html", locals())

def listTeams(request):
  teams = Team.objects.all()
  return render_to_response("listTeams.html", locals())

def listUsers(request):
  if 'team' in request.GET:
    users = User.objects.filter(team = Team.objects.get(id = int(request.GET['team'])))
  else:
    users = User.objects.all()
  return render_to_response("listUsers.html", locals())

def registerTeam(request):
  if request.method == 'POST':
    form = RegisterTeamForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      Team(name = cd['name'], bid = 0.0, ask = 0.0).save()
      # add to database
      return HttpResponseRedirect('/teams/register/thanks/')
  else:
    form = RegisterTeamForm()
  return render_to_response('registerTeam.html', locals())

def manager(request):
  teams = Team.objects.all()
      
  if request.method == 'POST':
    if 'reset' in request.POST:
      # delete all users, teams, transactions, queues
      User.objects.all().delete()
      Transaction.objects.all().delete()
      Queue.objects.all().delete()
      Team.objects.all().delete()
      News.objects.all().delete()
      status = "Deleted all data"
    else:
      form = ManagerUpdateForm(request.POST)
      if form.is_valid():
        cd = form.cleaned_data
        News(news = cd['news']).save()
        status = "Added news"
  else:
    form = ManagerUpdateForm()
    
  return render_to_response('manager.html', locals())

def loginUser(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      
      try:
        user = User.objects.get(name = cd['name'], email = cd['email'])
      except User.DoesNotExist:
        info = "There is no user with name %s and email %s" % (cd['name'], cd['email'])
      else:
        response = render_to_response('success', {'action': 'login'})
        response.set_cookie("user_id", user.id)
        return response
  else:
    form = LoginForm()
  return render_to_response('login.html', locals())
  
def registerUser(request):
  if request.method == 'POST':
    form = RegisterUserForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      
      # add to database
      user = User(name = cd['name'], email = cd['email'], team = cd['team'])
      user.save()
      
      response = HttpResponseRedirect('/users/register/thanks/')
      response.set_cookie("user_id", user.id)
      
      return response
  else:
    form = RegisterUserForm()
  return render_to_response('registerUser.html', locals())

def registerTeamThanks(request):
  return render_to_response('thanks.html', {'type': 'team'})

def registerUserThanks(request):
  return render_to_response('thanks.html', {'type': 'account'})

def ajax(request):
  if 'user_id' in request.COOKIES:
    try:
      user = User.objects.get(id = int(request.COOKIES['user_id']))
    except User.DoesNotExist:
      status = "Error: User with id %s does not exist" % request.COOKIES['user_id']
    else:
      status = "OK"
      if "action" in request.POST:
        action = request.POST["action"]
        if action == 'queue':
          try:
            team = Team.objects.get(id = int(request.POST['team_id']))
            queueItem = Queue.objects.get(trader = user)
          except Team.DoesNotExist:
            return HttpResponse("Error: Team with id %s does not exist" % request.POST['team_id'])
          except Queue.DoesNotExist:
            if "team_id" in request.POST and "market_action" in request.POST:
              Queue(trader = user, market = team, buying = (request.POST["market_action"] == "buy")).save()
            else:
              return HttpResponse("Error: Missing information")
          else:
            if (request.POST["market_action"] == "buy") == queueItem.buying and team == queueItem.market:
              queueItem.delete()
            else:
              queueItem.market = team
              queueItem.buying = (request.POST["market_action"] == "buy")
              queueItem.save()
        elif action == 'accept':
          try:
            queueItem = Queue.objects.filter(market = user.team)[0]
          except:
            status = "Error: Queue does not exist"
          else:
            if queueItem.buying: # trader was buying
              Transaction(price = user.team.ask, buyer = queueItem.trader, seller = user).save() # sell
              user.team.shares -= 1
              user.team.cash += user.team.ask
              user.team.save()
              
              queueItem.trader.team.cash -= user.team.ask
              queueItem.trader.team.shares += 1
              queueItem.trader.team.save()
            else: # trader selling; user buying
              Transaction(price = user.team.bid, buyer = user, seller = queueItem.trader).save()
              user.team.shares += 1
              user.team.cash -= user.team.bid
              user.team.save()
              
              queueItem.trader.team.cash += user.team.bid
              queueItem.trader.team.shares -= 1
              queueItem.trader.team.save()
            queueItem.delete()
        elif action == 'update_prices':
          if 'bid' in request.POST and 'ask' in request.POST:
            try:
              user.team.bid = float(request.POST['bid'])
              user.team.ask = float(request.POST['ask'])
            except ValueError:
              status = "Could not convert bid and ask to floats"
            else:
              user.team.save()
          else:
            status = "Error: Missing information"
      else:
        news = "\n".join(["<p>" + str(newsItem) + "</p>" for newsItem in News.objects.all()])
        waitingInQueue = "\n".join([("<li>%s</li>" % str(queueItem)) for queueItem in Queue.objects.filter(market = user.team)])
        teamAskBids = "\n".join(["%d|%.2f|%.2f|%d" % (team.id, team.bid, team.ask, len(Queue.objects.filter(market = team))) for team in Team.objects.all()])
        teamStatus = "%.2f|%d" % (user.team.cash, user.team.shares)
        status = DELIMETER.join([news, waitingInQueue, teamAskBids, teamStatus])#news + DELIMETER + waitingInQueue
  else:
    status = "Error: No user cookie"
  
  return HttpResponse(status)
    