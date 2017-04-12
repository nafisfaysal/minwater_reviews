from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.review_list, name='review_list'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    url(r'^mineralwater$', views.mineralwater_list, name='mineralwater_list'),
    url(r'^mineralwater/(?P<mineralwater_id>[0-9]+)/$', views.mineralwater_detail, name='mineralwater_detail'),
    url(r'^mineralwater/(?P<mineralwater_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]