from django.urls import path
from teams.views import TeamSpecificView, TeamView


urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<int:team_id>/", TeamSpecificView.as_view()),
]
