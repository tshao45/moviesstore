from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('petition/create/', views.view_petitions, name='movies.view_petitions'),
    path('petition/<int:petition_id>/approve/', views.approve_petition, name='movies.approve_petition'),

    

]