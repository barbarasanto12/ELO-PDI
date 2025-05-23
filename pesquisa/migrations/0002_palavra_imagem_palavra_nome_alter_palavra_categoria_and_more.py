# Generated by Django 5.1.7 on 2025-04-19 21:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pesquisa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='palavra',
            name='imagem',
            field=models.ImageField(default='utilizador/images/default.jpg', upload_to='palavras/'),
        ),
        migrations.AddField(
            model_name='palavra',
            name='nome',
            field=models.CharField(default='Nome padrão', max_length=100),
        ),
        migrations.AlterField(
            model_name='palavra',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pesquisa.categoria'),
        ),
        migrations.AlterField(
            model_name='palavra',
            name='texto',
            field=models.TextField(),
        ),
    ]
