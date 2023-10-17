from rest_framework.views import APIView, Response, Request, status
from django.forms.models import model_to_dict
from exceptions import ImpossibleTitlesError, InvalidYearCupError
from exceptions import NegativeTitlesError
from teams.models import Team
from utils import data_processing


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        team_data = request.data
        try:
            data_processing(team_data)
            team = Team.objects.create(**team_data)
        except NegativeTitlesError as err:
            print(err.message)
            return Response({"error": err.message}, 400)
        except InvalidYearCupError as err:
            print(err.message)
            return Response({"error": err.message}, 400)
        except ImpossibleTitlesError as err:
            print(err.message)
            return Response({"error": err.message}, 400)

        return Response(model_to_dict(team), 201)

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        teams_dict = [model_to_dict(team) for team in teams]
        return Response(teams_dict, 200)


class TeamSpecificView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(pk=team_id)
            team_dict = model_to_dict(team)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)
        return Response(team_dict, 200)

    def patch(self, request: Request, team_id: int) -> Response:
        team_data = request.data
        try:
            team = Team.objects.get(pk=team_id)
            for key in team_data:
                setattr(team, key, team_data[key])
            team.save()
            team_dict = model_to_dict(team)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        return Response(team_dict, 200)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            Team.objects.get(pk=team_id).delete()
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, 404)

        return Response(None, status.HTTP_204_NO_CONTENT)
