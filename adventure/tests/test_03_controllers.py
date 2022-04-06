import pytest
from django.core import mail
from django.utils import timezone
from adventure import models, notifiers, repositories, usecases, views

from .test_02_usecases import MockJourneyRepository


#########
# Tests #
#########


class TestRepository:
    def test_create_vehicle(self, mocker):
        mocker.patch.object(models.Vehicle.objects, "create")
        repo = repositories.JourneyRepository()
        car = models.VehicleType()
        repo.create_vehicle(name="a", passengers=10, vehicle_type=car)
        assert models.Vehicle.objects.create.called


class TestNotifier:
    def test_send_notification(self, mocker):
        mocker.patch.object(mail, "send_mail")
        notifier = notifiers.Notifier()
        notifier.send_notifications(models.Journey())
        assert mail.send_mail.called


class TestCreateVehicleAPIView:
    def test_create(self, client, mocker):
        vehicle_type = models.VehicleType(name="car")
        mocker.patch.object(
            models.VehicleType.objects, "get", return_value=vehicle_type
        )
        mocker.patch.object(
            models.Vehicle.objects,
            "create",
            return_value=models.Vehicle(
                id=1, name="Kitt", passengers=4, vehicle_type=vehicle_type
            ),
        )
        payload = {"name": "Kitt", "passengers": 4, "vehicle_type": "car"}
        response = client.post("/api/adventure/create-vehicle/", payload)
        assert response.status_code == 201


class TestStartJourneyAPIView:
    def test_api(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        payload = {"name": "Kitt", "passengers": 2}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 201

    def test_api_fail(self, client, mocker):
        mocker.patch.object(
            views.StartJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        payload = {"name": "Kitt", "passengers": 6}
        response = client.post("/api/adventure/start/", payload)

        assert response.status_code == 400


class TestStopJourneyAPIView:
    def test_stop(self, client, mocker):
        # TODO: Implement an endpoint that makes use of a StopJourney use case
        # and tests it

        mocker.patch.object(
            views.StopJourneyAPIView,
            "get_object",
            return_value=models.Journey(
                id=1, start=timezone.now().date()
            ),
        )

        mocker.patch.object(
            views.StopJourneyAPIView,
            "get_repository",
            return_value=MockJourneyRepository(),
        )

        response = client.put("/api/adventure/end/{}".format(1))

        assert response.status_code == 200
