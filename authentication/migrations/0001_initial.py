# Generated by Django 2.1.4 on 2019-01-30 17:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('f_name', models.CharField(max_length=255, verbose_name='first name')),
                ('m_name', models.CharField(max_length=255, verbose_name='middel name')),
                ('l_name', models.CharField(max_length=255, verbose_name='last name')),
                ('sex', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=2)),
                ('img', models.ImageField(default='admin-avatar.png', max_length=255, upload_to='profile', verbose_name='Photo')),
                ('u_name', models.CharField(max_length=255, unique=True, verbose_name='user name')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format : 09******** or +2519********', regex='^\\+?1?\\d{10,15}$')], verbose_name='phone')),
                ('is_admin', models.BooleanField(default=False)),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='date of birth')),
                ('place_of_birth', models.CharField(blank=True, max_length=100, null=True, verbose_name='place of birth')),
                ('disablity', models.CharField(choices=[('d', 'No Disable'), ('e', 'Eay Disable')], default='d', max_length=2)),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='city')),
                ('subcity', models.CharField(blank=True, max_length=255, null=True, verbose_name='subcity')),
                ('wereda', models.CharField(blank=True, max_length=255, null=True, verbose_name='wereda')),
                ('home_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='home number')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ManyToManyField(related_name='membership', to='authentication.Role'),
        ),
    ]