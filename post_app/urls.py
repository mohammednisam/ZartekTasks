from django.conf.urls import url
from  .views import PostViewSets
urlpatterns = [
    url(r'^add-post/$',PostViewSets.as_view({'get':'list','post':'create'}),name='sales'),
    url(r'^add-post/(?P<pk>\d+)/$',PostViewSets.as_view({'patch':'update','put':'retrieve'}),name='sales'),
]
