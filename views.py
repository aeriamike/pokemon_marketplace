from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from notifications.signals import notify
import datetime
from users.models import UserProfile
from django.contrib.auth.decorators import login_required

# from .models import TradePost as TradePost_Model
# from .models import pokemon as Pokemon


from django.utils import timezone

import datetime
from .models import TradePost, Pokemon, OfferTrade, Favourite, PokeAbilities
pkgames = ["Red", "Blue", "Yellow", "Gold", "Silver", "Crystal", "Ruby", "Sapphire", "Emerald", "FireRed", "LeafGreen", "Diamond", "Pearl", "Platinum", "HeartGold", "SoulSilver", "Black", "White", "Colosseum", "XD", "Black-2", "White-2", "X", "Y"]
pokemon = Pokemon.objects.order_by('name')
pokeabilities = PokeAbilities.objects.order_by('name')
pktypes = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]
pktypes = sorted(pktypes)
pkgames = sorted(pkgames)

# Create your views here.

def index(request):
    user = request.user

    # loader.get_template('pokemon/index.html')
    # print (request.tradepost.trader)
    print ("profile 0")
    now = datetime.datetime.now()
    #pokemon = Pokemon.objects.all()
    tradepost = TradePost.objects.all()
    #pokeabilities = PokeAbilities.objects.all()


    #tradepost = TradePost.objects.all()
    #return HttpResponse("Hello, world. You are at the Pokemon Marketplace.")
    favo = Favourite.objects.filter(trader_id = user.id ).values('post_id')
    print(favo)
    print(now - datetime.timedelta(days=2))
    #tradepost = TradePost.objects.exclude(trader=user.username).filter(Deadline__gte = (now - datetime.timedelta(days=2)))
    #tradepost = TradePost.objects.exclude(pk__in = favo).filter(Deadline__gte = (now - datetime.timedelta(days=0)))
    tradepost = TradePost.objects.exclude(pk__in = favo)

    print(tradepost)
    pkid = "0"
    pkname = "0"
    pktype = "0"
    pkgame = "0"
    pkability = "0"

    trader = "0"
    pokemon_offer = "0"
    gender = "0"
    level = "0"
    game = "0"
    deadline = "0"
    tradepost = tradepost.order_by('pk')
    if request.method == 'GET':
        reverse = ''
        getter = request.GET
        if len(getter) > 0:
                
            if getter.get('trader') != None:
                trader = getter.get('trader')
                if trader == "0":
                    trader = "1"
                else:
                    trader = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'trader')
            elif getter.get('pokemon_offer') != None:
                pokemon_offer = getter.get('pokemon_offer')
                if pokemon_offer == "0":
                    pokemon_offer = "1"
                else:
                    pokemon_offer = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'pokemon_name')
            elif getter.get('gender') != None:
                gender = getter.get('gender')
                if gender == "0":
                    gender = "1"
                else:
                    gender = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'pokemon_gender')
            elif getter.get('level') != None:
                level = getter.get('level')
                if level == "0":
                    level = "1"
                else:
                    level = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'pokemon_level')
            elif getter.get('game') != None:
                game = getter.get('game')
                if game == "0":
                    game = "1"
                else:
                    game = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'game')
            elif getter.get('deadline') != None:
                deadline = getter.get('deadline')
                if deadline == "0":
                    deadline = "1"
                else:
                    deadline = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'deadline')
                
    elif request.method == 'POST':
        if 'pkid' in request.POST:
            pkid = request.POST['pkid']
            tradepost = tradepost.filter(pokemon_id=str(pkid).zfill(3))
            print ("profile 1")
        elif 'pkname' in request.POST:
            pkname = request.POST['pkname']
            tradepost = tradepost.filter(pokemon_name=pkname)
        elif 'pktype' in request.POST:
            pktype = request.POST['pktype']
            tradepost = tradepost.filter(pokemon_types__contains=[pktype])
        elif 'pkgame' in request.POST:
            pkgame = request.POST['pkgame']
            tradepost = tradepost.filter(game=pkgame)
            print ("profile 2")
        elif 'pkability' in request.POST:
            pkability = request.POST['pkability']
            tradepost = tradepost.filter(pokemon_abilities__contains=[pkability])

    return render(request, 'pokemon/index.html',{
            'tradepost':tradepost,'pokemon':pokemon, 'pokeabilities': pokeabilities, 'pktype':pktypes, 'pkgame': pkgames,
            '1pk': {'id':pkid, 'name':pkname, 'type':pktype, 'game':pkname, 'ability':pkability},
            'queryString': "&pkid="+pkid+"&pkname="+pkname+"&pktype="+pktype+"&pkgame="+pkgame+"&pkability="+pkability,
            'toggle': {'trader': trader, 'pokemon_offer': pokemon_offer, 'gender': gender, 'level': level, 'game': game, 'deadline': deadline},
            "unread_count": request.user.notifications.unread().count() if user.is_authenticated else 0,
            "notifications": request.user.notifications.all() if user.is_authenticated else {}
            })


@login_required
def profile(request):
    print ("fav")
    user = request.user
    # from notifications.signals import notify
    # notify.send(user, recipient=user, verb="Notification")

    fcode = "0"
    if user.is_authenticated:
        # current_user = request.user
        fcode = UserProfile.objects.get(user_name=user.username)

        print (user.id)
        print(user.email)
        print(user.username)
        print("hello world 2")

    incomplete_tradepost = TradePost.objects.filter(trader=user.username)#.filter(completed_by=user.username)
    completed_post = TradePost.objects.filter(completed_by=user.username)

    tradepost = incomplete_tradepost.union(completed_post)
    tradepost = tradepost.order_by('pk')
    favourite = Favourite.objects.filter(trader_name=user.username)
    offertrade = OfferTrade.objects.filter(trader=user.username)

    return render(
        request,
        "pokemon/profile.html/",
        {"tradepost": tradepost, "offertrade": offertrade, "favourite": favourite, "fcode": fcode},
    )


def resource(request):

    # loader.get_template('pokemon/index.html')

    # return HttpResponse("Hello, world. You are at the Pokemon Marketplace.")
    return render(request, "pokemon/resource.html")

def tradelist(request):
    user = request.user


    #loader.get_template('pokemon/index.html')
    #pokemon = Pokemon.objects.all()
    #pokeabilities = PokeAbilities.objects.all()

    now = datetime.datetime.now()

    favo = Favourite.objects.filter(trader_id = user.id ).values('post_id')
    print(favo)
    print(now - datetime.timedelta(days=2))
    #tradepost = TradePost.objects.exclude(trader=user.username).filter(Deadline__gte = (now - datetime.timedelta(days=2)))
    tradepost = TradePost.objects.exclude(pk__in = favo)
    #tradepost = TradePost.objects.all()

    pkid = "0"
    pkname = "0"
    pktype = "0"
    pkgame = "0"
    pkability = "0"

    trader = "0"
    pokemon_offer = "0"
    gender = "0"
    level = "0"
    game = "0"
    deadline = "0"

    tradepost = tradepost.order_by('pk')

    if request.method == 'GET':
        reverse = ''
        getter = request.GET
        if len(getter) > 0:
            if getter.get('pkid') != '0':
                pkid = getter.get('pkid')
                tradepost = tradepost.filter(pokemon_id=str(pkid).zfill(3))
            elif getter.get('pkname') != '0':
                pkname = getter.get('pkname')
                tradepost = tradepost.filter(pokemon_name=pkname)
            elif getter.get('pktype') != '0':
                pktype = getter.get('pktype')
                tradepost = tradepost.filter(pokemon_types__contains=[pktype])
            elif getter.get('pkgame') != '0':
                pkgame = getter.get('pkgame')
                tradepost = tradepost.filter(game=pkgame)
            elif getter.get('pkability') != '0':
                pkability = getter.get('pkability')
                tradepost = tradepost.filter(pokemon_abilities__contains=[pkability])
                
            if getter.get('trader') != None:
                trader = getter.get('trader')
                if trader == "0":
                    trader = "1"
                else:
                    trader = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'trader')
            elif getter.get('pokemon_offer') != None:
                pokemon_offer = getter.get('pokemon_offer')
                if pokemon_offer == "0":
                    pokemon_offer = "1"
                else:
                    pokemon_offer = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'pokemon_name')
            elif getter.get('gender') != None:
                gender = getter.get('gender')
                if gender == "0":
                    gender = "1"
                else:
                    gender = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'pokemon_gender')
            elif getter.get('level') != None:
                level = getter.get('level')
                if level == "0":
                    level = "1"
                else:
                    level = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'pokemon_level')
            elif getter.get('game') != None:
                game = getter.get('game')
                if game == "0":
                    game = "1"
                else:
                    game = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'game')
            elif getter.get('deadline') != None:
                deadline = getter.get('deadline')
                if deadline == "0":
                    deadline = "1"
                else:
                    deadline = "0"
                    reverse = "-"
                tradepost = tradepost.order_by(reverse+'deadline')
                
    elif request.method == 'POST':
        if 'pkid' in request.POST:
            pkid = request.POST['pkid']
            tradepost = tradepost.filter(pokemon_id=str(pkid).zfill(3))
        elif 'pkname' in request.POST:
            pkname = request.POST['pkname']
            tradepost = tradepost.filter(pokemon_name=pkname)
        elif 'pktype' in request.POST:
            pktype = request.POST['pktype']
            tradepost = tradepost.filter(pokemon_types__contains=[pktype])
        elif 'pkgame' in request.POST:
            pkgame = request.POST['pkgame']
            tradepost = tradepost.filter(game=pkgame)
        elif 'pkability' in request.POST:
            pkability = request.POST['pkability']
            tradepost = tradepost.filter(pokemon_abilities__contains=[pkability])

    return render(request, 'pokemon/tradelist.html',{
            'tradepost':tradepost,'pokemon':pokemon, 'pokeabilities': pokeabilities, 'pktype':pktypes, 'pkgame': pkgames,
            '1pk': {'id':pkid, 'name':pkname, 'type':pktype, 'game':pkname, 'ability':pkability},
            'queryString': "&pkid="+pkid+"&pkname="+pkname+"&pktype="+pktype+"&pkgame="+pkgame+"&pkability="+pkability,
            'toggle': {'trader': trader, 'pokemon_offer': pokemon_offer, 'gender': gender, 'level': level, 'game': game, 'deadline': deadline}
            })

def pokelocator(request):
    pokemon = Pokemon.objects.order_by("id")
    return render(request, "pokemon/pokelocator.html", {"pokemon": pokemon})


def maketrade(request):
    if request.method == 'GET':
        pokemon_list = Pokemon.objects.order_by('id')
        return render(request, 'pokemon/maketrade.html', {'pokemon_list': pokemon_list, 'pkgames': pkgames})
    else:
        data = request.POST
        pkData = data['pkData'].split(' - ')
        user = request.user
        deadline = timezone.now() + datetime.timedelta(days=3)
        pokemon = Pokemon.objects.get(id=int(pkData[0]))
        tradepost = TradePost(
            trader=user.username,
            pokemon_name=pkData[1],
            pokemon_id=int(pkData[0]),
            pokemon_types=pokemon.types,
            pokemon_abilities=pokemon.abilities,
            pokemon_gender=data["pkGender"],
            pokemon_level=data["pkLevel"],
            game=data["pkGame"],
            deadline=deadline,
        )
        tradepost.save()
        return HttpResponseRedirect(reverse('pokemon:profile'))

@login_required
def offertrade(request, post_id):

    print (post_id)
    tradepost = get_object_or_404(TradePost, pk=post_id)
    user = request.user
    # Need to see whether it has been expired or traded, if yes, we need to redirect the page.
    if tradepost.traded_date is not None:
        return render(request, 'pokemon/offertrade.html', {'error_message': 'This trade post has been completed.'})

    if request.method == 'GET':
        pokemon_list = Pokemon.objects.order_by('id')
        # Need to check if the post is the current user's post or not
        if tradepost.trader != user.username:
            return render(
                request,
                "pokemon/offertrade.html",
                {"tradepost": tradepost, "pokemon_list": pokemon_list, 'pkgames': pkgames},
            )
        else:
            return render(request, 'pokemon/offertrade.html', {'error_message': "User are prohibited to offer trade with the same user."})
    else:
        # For POST request
        data = request.POST
        pkData = data["pkData"].split(" - ")
        pokemon = Pokemon.objects.get(id=int(pkData[0]))
        offertrade = tradepost.offertrade_set.create(
            post_id=post_id,
            trader=user.username,
            pokemon_id=int(pkData[0]),
            pokemon_name=pkData[1],
            pokemon_types=pokemon.types,
            pokemon_abilities = pokemon.abilities,
            pokemon_gender=data["pkGender"],
            pokemon_level=data["pkLevel"],
            game = data['pkGame'],
        )
        offertrade.save()
        notify.send(user, recipient=User.objects.get(username=tradepost.trader), verb= user.username + " has send an offer!")

        return HttpResponseRedirect(reverse('pokemon:profile'))

# TODO: Need to make a page to put offer and the post into a page (Accept or Decline page)
# TODO: Template, View, (maybe model?)
def sentoffer(request, offer_id):
    offer = get_object_or_404(OfferTrade, pk=offer_id)
    user = request.user
    tradepost = offer.post

    if request.method == 'GET':
        if offer.state != '':
            return render(request, 'pokemon/sentoffer.html', {'error_message': 'Sorry this offer page has been removed.'})
        else:
            return render(request, 'pokemon/sentoffer.html', {'tradepost': tradepost, 'offer': offer})
    else:
        # Prevent two accepted offer
        if tradepost.traded_date is None:
            if 'accepted' in request.POST:
                print("offer notify")
                notify.send(user, recipient=User.objects.get(username=offer.trader), verb= user.username + " accepted your offer!")
                
                offer.state = 'accepted'    
                # Need to decline other offers inside the post.
                offers = tradepost.offertrade_set.filter(state='').exclude(pk=offer.pk)
                for curr_offer in offers:
                    if curr_offer.trader != offer.trader:
                        notify.send(user, recipient=User.objects.get(username=curr_offer.trader), verb="The post has been completed! Your offer will be removed.")
                    curr_offer.state = 'declined'
                    curr_offer.save()
                tradepost.traded_date = timezone.now()
                tradepost.completed_by = offer.trader
                tradepost.save()
            elif 'declined' in request.POST:
                notify.send(user, recipient=User.objects.get(username=offer.trader), verb= user.username + " declined your offer!")
                offer.state = 'declined'
            offer.save()
        return HttpResponseRedirect(reverse('pokemon:profile'))
            # render(request, 'pokemon/profile.html', {'tradepost': TradePost.objects.filter(trader=user.username)})

def chat(request):

    # loader.get_template('pokemon/index.html')

    # return HttpResponse("Hello, world. You are at the Pokemon Marketplace.")
    return render(request, "pokemon/chat.html")


def notification(request):

    # loader.get_template('pokemon/index.html')

    # return HttpResponse("Hello, world. You are at the Pokemon Marketplace.")
    return render(request, "pokemon/notification.html")

@login_required
def favourite(request, post_id):
    current_user = request.user
    if current_user.is_authenticated:
        if request.GET.get("Delete"):
            Favourite.objects.filter(pk=post_id).delete()
        elif request.GET.get("favourite"):
            username = current_user.username
            user_id = current_user.id
            fav = request.GET.get("favourite")
            tradepost = TradePost.objects.get(pk=post_id)

            favourite = tradepost.favourite_set.create(
                post_id = post_id,
                trader_id = user_id,
                trader_name = username,
            )
            favourite.save()
            tradepost.save()

            favi = Favourite.objects.filter(trader_name=username).values()

        past_url = request.META['HTTP_REFERER'].split('?')[0]
        redirect_url = ':'.join(past_url.split('/')[3:-1])
        if redirect_url == 'pokemon': redirect_url = redirect_url + ':index' 
        return HttpResponseRedirect(reverse(redirect_url))