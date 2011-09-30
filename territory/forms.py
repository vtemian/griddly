from django.forms import ModelForm
from territory.models import Territory

class ChangeName(ModelForm):
    class Meta:
         model = Territory
         fields = ('name',)
