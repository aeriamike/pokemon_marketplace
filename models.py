from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.utils import timezone

# Create your models here.

class TradePost(models.Model):
    trader = models.CharField(max_length=200)
    pokemon_name = models.CharField(max_length=200)
    pokemon_id = models.IntegerField()
    pokemon_types = ArrayField(models.CharField(max_length=30), null=True)
    pokemon_abilities = ArrayField(models.CharField(max_length=30), null=True)
    pokemon_level = models.IntegerField(default=1)
    pokemon_gender = models.CharField(max_length=50, default="Male")
    game = models.CharField(max_length=200, default="Red")
    completed_by = models.CharField(max_length=200, default="")
    traded_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField()

    def is_active(self):
        return self.traded_date is None and self.deadline >= timezone.now()
        
    def past_expiration(self):
        return self.deadline < timezone.now()

#red
#gottacatchemall

class OfferTrade(models.Model):
    post = models.ForeignKey(TradePost, on_delete=models.CASCADE, default=1)
    trader = models.CharField(max_length=200)
    pokemon_id = models.IntegerField()
    pokemon_name = models.CharField(max_length=200)
    pokemon_types = ArrayField(models.CharField(max_length=30), null=True)
    pokemon_abilities = ArrayField(models.CharField(max_length=30), null=True)
    pokemon_gender = models.CharField(max_length=200, default="Male")
    pokemon_level = models.IntegerField(default=1)
    game = models.CharField(max_length=200)
    state = models.CharField(max_length=20, default="")
    
    def is_available(self):
        return self.state == ""

    def is_accepted(self):
        return self.state == "accepted"

class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    types = ArrayField(models.CharField(max_length=30, null=True, blank=True), null=True)
    abilities = ArrayField(models.CharField(max_length=30, null=True, blank=True), null=True)
    # https://docs.djangoproject.com/en/2.2/ref/contrib/postgres/fields/#querying-jsonfield
    encounters = JSONField(null=True)

class PokemonTypes(models.Model):
    types = models.CharField(max_length=200)

class Favourite(models.Model):
    post = models.ForeignKey(TradePost, on_delete=models.CASCADE, default=1)
    trader_id  = models.IntegerField()
    trader_name  = models.CharField(max_length=200)

class PokeAbilities(models.Model):
    name = models.CharField(max_length=200)

