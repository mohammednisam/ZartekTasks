from django.conf.urls import url
from  .views import UserLoginViewSet,UserViewSet
urlpatterns = [
    url(r'^add-user/$',UserViewSet.as_view({'get':'list'}),name='add-user'),
    url(r'^login/$',UserLoginViewSet.as_view({'get':'list','post':'post'}),name='login'),
]