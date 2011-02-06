from django import forms
from pitSimulator.PitSimulator.models import *

class RegisterTeamForm(forms.Form):
  name = forms.CharField(label = "Your team name", max_length = 100)

class RegisterUserForm(forms.Form):
  name = forms.CharField(max_length = 100)
  email = forms.EmailField()
  team = forms.ModelChoiceField(queryset = Team.objects.all())#forms.ChoiceField(choices = [(row.id, row.name) for row in Team.objects.all()])
  
class LoginForm(forms.Form):
  name = forms.CharField(max_length = 100)
  email = forms.EmailField()
  
class ManagerUpdateForm(forms.Form):
  news = forms.CharField(widget = forms.Textarea)