# Generated by Django 4.0.1 on 2022-02-08 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_remove_hotelcontact_hotel_remove_hotelphoto_hotel_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default='')),
                ('room_number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoomReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=50)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('phone_number', models.CharField(max_length=20)),
                ('room_number', models.PositiveIntegerField()),
                ('qr_photo', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_type', models.CharField(choices=[('single', 'Single'), ('double', 'Double'), ('trible', 'Trible')], max_length=15)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoomPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.CharField(max_length=100)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.hotelroom')),
            ],
        ),
        migrations.CreateModel(
            name='HotelRoomExtension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.hotelroom')),
            ],
        ),
        migrations.AddField(
            model_name='hotelroom',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.hotelroomtype'),
        ),
        migrations.CreateModel(
            name='HotelPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.CharField(max_length=100)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='HotelContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_type', models.CharField(choices=[('email', 'Email'), ('phone', 'Phone')], max_length=10)),
                ('content', models.CharField(max_length=50)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hotel')),
            ],
        ),
    ]
