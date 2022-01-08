from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from account.models import Account

class the2048(models.Model):
    user         = ForeignKey(Account, on_delete=models.CASCADE)
    time_start   = models.DateTimeField(blank=True, null=True)
    time_end     = models.DateTimeField(blank=True, null=True)
    duration     = IntegerField(blank=True, null=True)
    duration_name= models.CharField(max_length=100, blank=True, null=True)
    score        = IntegerField()
    highest_tile = IntegerField()
    moves        = IntegerField()

    def __str__(self):
        return self.user.username + " - " + str(self.score)
    
    class Meta:
       ordering = ['-score']
