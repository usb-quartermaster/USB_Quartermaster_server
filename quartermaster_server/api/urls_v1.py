"""quartermaster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from .views import ResourceDetail, ReservationDjangoAuthView, ReservationResourcePasswordView, Login, ResourceList, \
    PoolList, PoolResourceList

urlpatterns = [
    path('login', Login.as_view(), name="login_status"),
    path("pool/", PoolList.as_view(), name='list_pools'),
    path("pool/<str:pool_pk>/", PoolResourceList.as_view(), name='list_pool_resources'),
    path("resource/", ResourceList.as_view(), name='list_resources'),
    path("resource/<str:resource_pk>", ResourceDetail.as_view(), name='show_resource'),
    path("resource/<str:resource_pk>/reservation",
         ReservationDjangoAuthView.as_view(), name='show_reservation'),
    path("resource/<str:resource_pk>/reservation/<str:resource_password>",
         ReservationResourcePasswordView.as_view(), name='show_reservation_with_password')
]
