
from django.urls import path
from classapp import views
# from classapp.views import AboutView

urlpatterns = [
    # path('about/', views.about, name="about"),
    # path('sendmail/', views.sendmail, name="smail"),
    # path('thanks/', views.thanks, name="thanks"),
    path('', views.PersonListView.as_view(), name='person_changelist'),
    path('add/', views.personprofile, name='person_add'),
    path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),
    path('ajax/load-cities/', views.load_cities,
         name='ajax_load_cities'),  # <-- this one here
]
