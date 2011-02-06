from django.db import models

# Create your models here.
class Team(models.Model):
  name = models.CharField(max_length = 100, unique = True)
  bid = models.FloatField()
  ask = models.FloatField()
  shares = models.IntegerField(default = 0)
  cash = models.FloatField(default = 0.0)
  
  def __unicode__(self):
    return self.name

class User(models.Model):
  name = models.CharField(max_length = 100, unique = True)
  email = models.EmailField(unique = True)
  team = models.ForeignKey(Team)
  
  def __unicode__(self):
    return u"%s (Team %s, Email %s)" % (self.name, self.team, self.email)

class News(models.Model):
  time = models.DateTimeField(auto_now_add = True)
  news = models.TextField()
  
  def __unicode__(self):
    return u"%s -- %s" % (self.time, self.news)
  
class Transaction(models.Model):
  time = models.DateTimeField(auto_now_add = True)
  price = models.FloatField()
  buyer = models.ForeignKey(User, related_name = 'buyer_id')
  seller = models.ForeignKey(User, related_name = 'seller_id')
  
  def __unicode__(self):
    return u"%s purchased from %s at %lf on %s" % (self.buyer, self.seller, self.price, self.time)

class Queue(models.Model):
  waiting_since = models.DateTimeField(auto_now_add = True)
  trader = models.ForeignKey(User, unique = True)
  market = models.ForeignKey(Team)
  buying = models.BooleanField() # true if buying, false if selling
  
  def __unicode__(self):
    if self.buying:
      action = "buy"
    else:
      action = "sell"
    return (u"%s waiting to %s since %s" % (self.trader, action, self.waiting_since))
  
  class Meta:
    ordering = ['id']