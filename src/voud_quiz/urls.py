from django.conf.urls import url
from .views import *
urlpatterns =[
	url(r'^$',QuizListView.as_view(),name='quiz_index'),
	url(r'^(?P<slug>[\w-]+)/$',QuizDetailView.as_view(),name='quiz_start_page'),
	url(r'^(?P<quiz_name>[\w-]+)/take/$',QuizTake.as_view(),name='quiz_question'),

]