# Generated by Django 4.2 on 2024-03-27 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default=None, upload_to='')),
                ('name', models.CharField(default=None, max_length=255)),
                ('type', models.CharField(choices=[('RAR', 'RAR'), ('ZIP', 'ZIP'), ('PNG', 'PNG'), ('JPEG', 'JPEG')], default=None, max_length=10)),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('uui', models.CharField(default=None, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.usersession')),
                ('clear_cache', models.BooleanField(default=True)),
                ('hide_text', models.BooleanField(default=False)),
                ('mse', models.BooleanField(default=True)),
                ('ssim', models.BooleanField(default=True)),
                ('vgg16', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comparation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now=True)),
                ('update', models.DateTimeField(blank=True, default=None, null=True)),
                ('method', models.CharField(blank=True, choices=[('MSE', 'MSE'), ('SSIM', 'SSIM'), ('VGG16', 'VGG16')], default=None, max_length=10, null=True)),
                ('threshold', models.IntegerField(blank=True, default=None, null=True)),
                ('is_similar', models.BooleanField(blank=True, default=None, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.usersession', to_field='user_id')),
            ],
        ),
    ]
