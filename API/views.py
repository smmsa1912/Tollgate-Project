import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Core.models import Exit_Point, TollRecord, VehicleEntry, Vehicle
from geopy.distance import geodesic


# Create your views here.

def calculate_distance(entry_point, exit_point):
    entry_coords = (entry_point.Latitude, entry_point.Longitude)
    exit_coords = (exit_point.Latitude, exit_point.Longitude)
    return geodesic(entry_coords, exit_coords).kilometers


class ExitPointsView(APIView):
    def post(self, request, exit_id, rfid):
        exit_point = Exit_Point.objects.filter(Exit_Point_ID=exit_id).first()
        vehicle = Vehicle.objects.filter(RFID=rfid).first()
        vehicle_entry = VehicleEntry.objects.filter(Vehicle=vehicle).last()

        if not exit_point or not vehicle or not vehicle_entry:
            return Response({"error": "Invalid exit point ID, RFID, or no entry record found."},
                            status=status.HTTP_400_BAD_REQUEST)

        distance = calculate_distance(vehicle_entry.Entry_Camera, exit_point)
        toll_amount = distance * exit_point.Charges_Per_KM
        toll_amount = round(toll_amount, 2)
        distance = round(distance, 2)

        data = {}
        data.update({"distance_travelled": distance})
        data.update({"car_number": vehicle.Car_Number})
        data.update({"total_charge": toll_amount})
        data.update({"charge_per_km_cars": exit_point.Charges_Per_KM})
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_lobby',
            {
                'type': 'chat_message',
                'message': json.dumps(data)
            }
        )

        toll_record = TollRecord.objects.create(
            Vehicle=vehicle,
            Entry_Point=vehicle_entry.Entry_Camera,
            Exit_Point=exit_point,
            Distance_Traveled_KM=distance,
            Toll_Charged=toll_amount,
            Raw_Car_Number=vehicle_entry.Raw_Car_Number
        )

        toll_record.save()
        VehicleEntry.objects.filter(Vehicle=vehicle).delete()

        return Response({"toll_amount": toll_amount, "distance": distance}, status=status.HTTP_200_OK)
