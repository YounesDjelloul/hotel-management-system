# Generated by Django 4.0.1 on 2022-02-08 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_hotel_description_alter_hotel_lat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelcontact',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='hotelphoto',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='hotelroom',
            name='room_type',
        ),
        migrations.RemoveField(
            model_name='hotelroomextension',
            name='room',
        ),
        migrations.RemoveField(
            model_name='hotelroomphoto',
            name='room',
        ),
        migrations.DeleteModel(
            name='HotelRoomReservation',
        ),
        migrations.RemoveField(
            model_name='hotelroomtype',
            name='hotel',
        ),
        migrations.DeleteModel(
            name='HotelContact',
        ),
        migrations.DeleteModel(
            name='HotelPhoto',
        ),
        migrations.DeleteModel(
            name='HotelRoom',
        ),
        migrations.DeleteModel(
            name='HotelRoomExtension',
        ),
        migrations.DeleteModel(
            name='HotelRoomPhoto',
        ),
        migrations.DeleteModel(
            name='HotelRoomType',
        ),
    ]