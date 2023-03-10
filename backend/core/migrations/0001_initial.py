# Generated by Django 3.2.16 on 2023-03-09 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('dob', models.DateField(null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('heading', models.CharField(default='', max_length=255)),
                ('desc', models.TextField(default='')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CategoryService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Freelancing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('date_posted', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='freelancing_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('lat', models.IntegerField()),
                ('log', models.IntegerField()),
            ],
            options={
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VerifyTokenGen',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(max_length=8)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='token_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('lat', models.IntegerField()),
                ('log', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='location_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_range_availability', models.DateField()),
                ('end_range_availability', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FreelancingService',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('last_edited', models.DateTimeField(auto_now_add=True)),
                ('service_name', models.CharField(max_length=255)),
                ('payment_type', models.CharField(choices=[('HOUR', 'Hour'), ('ONCE', 'Once')], max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('freelancing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_freelancing', to='core.freelancing')),
            ],
            options={
                'ordering': ['-datetime_created'],
                'abstract': False,
            },
        ),
    ]
