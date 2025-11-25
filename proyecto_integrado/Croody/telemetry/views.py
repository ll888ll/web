from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import RobotPosition
from .utils import get_mock_traffic_data

class RobotPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RobotPosition
        fields = ['x', 'y', 'atmosphere', 'timestamp']

class RobotPositionViewSet(viewsets.ModelViewSet):
    queryset = RobotPosition.objects.all().order_by('-timestamp')
    serializer_class = RobotPositionSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request):
        latest = RobotPosition.objects.first()
        if latest:
            serializer = self.get_serializer(latest)
            return Response(serializer.data)
        return Response({})

def dashboard(request):
    return render(request, 'telemetry/dashboard.html')

def traffic_data(request):
    # In a real scenario, this would trigger analysis or read cached results.
    # For the prototype, we return mock data or read a static file.
    data = get_mock_traffic_data()
    return JsonResponse({'flows': data})
