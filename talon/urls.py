from django.urls import path
from talon.views import get_talons_1_2, get_branches, get_organizations, create_talon, update_talon

urlpatterns = [
    path('tables-1-2/', get_talons_1_2, name='get_talons_1_2'),
    path('branches/', get_branches, name='get_branches'),
    path('organizations/', get_organizations, name='get_organizations'),
    path('create/', create_talon, name='create_talon'),
    path('update/', update_talon, name='update_talon'),
]
