from django.urls import path
from .views import *
urlpatterns = [
    path('exit/<int:exit_id>/<str:rfid>/', ExitPointsView.as_view(), name='exit_point'),
]