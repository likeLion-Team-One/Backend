from groups.models import Team
from groups.serializers import HomeTeamSerializer, LatestTeamSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        progressing_groups = Team.objects.filter(members__user=user, progress__lt = 100).order_by('-id')[:5]
        completed_groups = Team.objects.filter(members__user=user, progress = 100).order_by('-id')[:5]
        latest_groups = Team.objects.order_by('-id')[:5]

        return Response({
            "progressing_groups": HomeTeamSerializer(progressing_groups, many=True).data,
            "completed_groups": HomeTeamSerializer(completed_groups, many=True).data,
            "latest_groups": LatestTeamSerializer(latest_groups, many=True).data,
        })

