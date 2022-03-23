# Generated by Django 4.0.3 on 2022-03-22 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_category_options_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=256)),
                ('subject', models.CharField(max_length=256)),
                ('message', models.TextField(max_length=1024)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-datetime']},
        ),
    ]
