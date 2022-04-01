from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from adventure import models, notifiers, repositories, serializers, usecases


class CreateVehicleAPIView(generics.CreateAPIView):
    serializer_class = serializers.VehicleSerializer

    def perform_create(self, serializer) -> Response:
        vehicle = models.Vehicle.objects.create(
            **serializer.validated_data
        )
        return Response(
            {
                "id": vehicle.id,
                "name": vehicle.name,
                "passengers": vehicle.passengers,
                "vehicle_type": vehicle.vehicle_type.name,
            },
            status=201,
        )


class StartJourneyAPIView(generics.CreateAPIView):
    serializer_class = serializers.JourneySerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.StartJourney(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except usecases.StartJourney.CantStart as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


class StopJourneyAPIView(generics.UpdateAPIView):
    serializer_class = serializers.JourneySerializer

    def put(self, request, *args, **kwargs):
        params = self.kwargs
        journey = models.Journey.objects.get(id=params["pk"])
        repo = self.get_repository()
        usecase = usecases.StopJourney(repo).set_params(journey)
        try:
            usecase.execute()
            return Response(
                {
                    "id": journey.id,
                    "start": journey.start,
                    "end": journey.end,
                },
                status=200,
            )
        except usecases.StopJourney.CantEnd as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()
