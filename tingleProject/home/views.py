from groups.models import Team
from groups.serializers import TeamListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, reqeust):
        progressing_groups = Team.objects.filter(progress__lt = 100).order_by('-id')[:5]
        completed_groups = Team.objects.filter(progress = 100).order_by('-id')[:5]
        latest_groups = Team.objects.order_by('-id')[:5]

        return Response({
            "progressing_groups": TeamListSerializer(progressing_groups, many=True).data,
            "completed_groups": TeamListSerializer(completed_groups, many=True).data,
            "latest_groups": TeamListSerializer(latest_groups, many=True).data,
        })

