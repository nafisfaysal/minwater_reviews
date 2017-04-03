from django.conf.urls import url
from .import views

urlpatterns = [
    #ex: /
    url(r'^$',views.review_list, name='review_list'),
    #ex: /review/5
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /mineralwater/
    url(r'^mineralwater$', views.mineralwater_list, name='mineralwater_list'),
    # ex: /mineralwater/5/
    url(r'^mineralwater/(?P<mineralwater_id>[0-9]+)/$', views.mineralwater_detail, name='mineralwater_detail'),
    url(r'^mineralwater/(?P<mineralwater_id>[0-9]+)/add_review/$', views.add_review,name='add_review')

]


