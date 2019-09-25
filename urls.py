from django.urls import include, path
from . import views

app_name = 'pokemon'
urlpatterns = [
    path('', views.index, name='index'),
    #path('<int:id>/', views.contactor, name='contactor'),
    #path('<int:id>/edit', views.edit, name='edit'),
    path('resource/', views.resource, name='resource'),
    path('profile/', views.profile, name='profile'),
    path('tradelist/', views.tradelist, name='tradelist'),
    path('pokelocator/', views.pokelocator, name='pokelocator'),
    path('profile/maketrade', views.maketrade, name='maketrade'),
    path('offertrade/', views.offertrade, name='offertrade'),
    path('messages/', include('privatemsg.urls', namespace='privatemsg')),
    path('offertrade/<int:post_id>', views.offertrade, name='offertrade'),
    path('notification/', views.notification, name='notification'),
    path('offers/<int:offer_id>', views.sentoffer, name='sentoffer'),

    path('favourite/<int:post_id>', views.favourite, name='favourite')






]
