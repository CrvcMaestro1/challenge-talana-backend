from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from adventure import models, notifiers, repositories, serializers, usecases


class CreateVehicleAPIView(generics.CreateAPIView):
    serializer_class = serializers.VehicleSerializer

    def perform_create(self, serializer) -> None:
        repo = self.get_repository()
        notifier = notifiers.Notifier()
        usecase = usecases.CreateVehicle(repo, notifier).set_params(
            serializer.validated_data
        )
        try:
            usecase.execute()
        except Exception as e:
            raise ValidationError({"detail": str(e)})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()


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
    serializer_class = serializers.JourneyDummySerializer
    queryset = models.Journey.objects

    def perform_update(self, serializer):
        repo = self.get_repository()
        usecase = usecases.StopJourney(repo).set_params(self.get_object())
        usecase.execute()

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        journey = self.get_object()
        return Response({"id": journey.id, "start": journey.start, "end": journey.end})

    def get_repository(self) -> repositories.JourneyRepository:
        return repositories.JourneyRepository()
