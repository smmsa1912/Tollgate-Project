from celery import shared_task
from Core.models import VehicleEntry, Vehicle, Camera


@shared_task
def add_vehicle_entry(car_number, camera_id):
    camera = Camera.objects.filter(Camera_ID=camera_id).first()
    if VehicleEntry.objects.filter(Raw_Car_Number=car_number, Entry_Camera=camera).exists():
        return f"Vehicle entry for car number: {car_number} at camera ID: {camera_id} already exists."
    vehicle = Vehicle.objects.filter(Car_Number=car_number).first()
    vehicle_entry = VehicleEntry.objects.create(
        Vehicle=vehicle,
        Raw_Car_Number=car_number,
        Entry_Camera=camera
    )
    vehicle_entry.save()
    return f"Added vehicle entry for car number: {car_number}"
