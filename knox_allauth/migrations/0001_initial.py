# Generated by Django 4.0.3 on 2022-03-31 14:27

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import imagekit.models.fields
import knox_allauth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(default=knox_allauth.models._createHash, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=50, verbose_name='first_name')),
                ('first_name', models.CharField(max_length=50, verbose_name='first_name')),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('sms', models.CharField(blank=True, max_length=15, null=True)),
                ('site_id', models.CharField(default=knox_allauth.models._createHash, max_length=50)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_creator', models.BooleanField(default=False)),
                ('profile_completed', models.BooleanField(default=False)),
                ('bio', models.CharField(max_length=500)),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('members', models.IntegerField(default=0)),
                ('followers', models.IntegerField(default=0)),
                ('earning', models.IntegerField(default=0)),
                ('profession', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=50)),
                ('member_since', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('picture', imagekit.models.fields.ProcessedImageField(default='ProfileDefaultImage.png', upload_to=knox_allauth.models.upload_path)),
                ('picture_medium', imagekit.models.fields.ProcessedImageField(default='ProfileDefaultImage.png', upload_to=knox_allauth.models.upload_path)),
                ('picture_small', imagekit.models.fields.ProcessedImageField(default='ProfileDefaultImage.png', upload_to=knox_allauth.models.upload_path)),
                ('picture_tag', imagekit.models.fields.ProcessedImageField(default='ProfileDefaultImage.png', upload_to=knox_allauth.models.upload_path)),
                ('address1', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 1')),
                ('address2', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Address line 2')),
                ('zip_code', models.CharField(blank=True, max_length=12, null=True, verbose_name='Postal Code')),
                ('city', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Kommun')),
                ('state', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Lansting')),
                ('country', models.CharField(blank=True, max_length=1024, null=True, verbose_name='contry')),
                ('Facebook_link', models.CharField(blank=True, help_text='Facebook_link', max_length=120, null=True)),
                ('twitter', models.CharField(blank=True, help_text='twitter', max_length=120, null=True)),
                ('Linkdin_link', models.CharField(blank=True, help_text='Linkdin_link', max_length=120, null=True)),
                ('othersSocialMedia', models.CharField(blank=True, help_text='Linkdin_link', max_length=120, null=True)),
                ('stripeCustomerId', models.CharField(blank=True, help_text='Linkdin_link', max_length=120, null=True)),
                ('subscriptionType', models.CharField(default='groundplan', max_length=10, verbose_name='subscriptionType of the user:')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('about', models.TextField(default='The user did not put any thing yet', max_length=120, verbose_name='Om mig')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', knox_allauth.models.UserManager()),
            ],
        ),
    ]
