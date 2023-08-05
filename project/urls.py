"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tickets import views

from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register('guests',views.ViewSet_gusts) 
router.register('movies',views.ViewSet_movi) 
router.register('reservations',views.ViewSet_reservation) 

urlpatterns = [
    path("admin/", admin.site.urls),
    
    #1 static data
    path("django/jsonresponsnomodel/",views.no_rest_no_model),
    #2 no  rest from model
    path("django/jsonresponsfrommodel/",views.no_rest_from_model),
    
    #3.1
    path("rest/fvblist/",views.FBV_List),
    
    #3.2
    path("rest/fvblist/<int:pk>",views.FBV_pk),
    
    #4.1 GET POST CLass based view
    path("rest/cvb/",views.CBV_List.as_view()),
    #4.2 GET PUT DELETE CLass based view
    path("rest/cvb/<int:pk>",views.CBV_pk.as_view()),
    
    #5.1 GET POST CLass based view using mixins
    path("rest/mixins/",views.Mixins_list.as_view()),
    #5.2 GET PUT DELETE CLass based view using mixins
    path("rest/mixins/<int:pk>",views.Mixins_pk.as_view()),
    
    #6.1 GET POST CLass based view using mixins
    path("rest/generic/",views.Generic_list.as_view()),
    #6.2 GET PUT DELETE CLass based view using mixins
    path("rest/generic/<int:pk>",views.Generic_pk.as_view()),
    
    # 7 viewset
    path("rest/viewset/",include(router.urls)),
    
    # 8 find movie
    path("fbv/findmovie",views.find_movie),
    
    # 9 find movie
    path("fbv/newresrvation",views.new_reservation),
    
]
