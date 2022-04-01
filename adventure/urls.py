from django.urls import path

from adventure import views

urlpatterns = [
    path("create-vehicle/", views.CreateVehicleAPIView.as_view(), name='create-vehicle'),
    path("start/", views.StartJourneyAPIView.as_view(), name='start'),
    path("end/<int:pk>", views.StopJourneyAPIView.as_view(), name='end'),
]
