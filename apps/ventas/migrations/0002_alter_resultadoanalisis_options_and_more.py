# Generated by Django 4.2.9 on 2024-02-04 18:34

import apps.ventas.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resultadoanalisis',
            options={'ordering': ['-fecha_analisis'], 'verbose_name': 'Analisis de predicciones', 'verbose_name_plural': 'Analisis de predicciones'},
        ),
        # migrations.RemoveField(
        #     model_name='nombre_del_modelo',
        #     name='created_at',
        # ),

        #migrations.RemoveField(
        #    model_name='venta',
        #    name='analizada',
        #),
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id_fase', models.CharField(default=apps.ventas.models.conver_encode, editable=False, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Rayado y corte', 'Rayado y corte'), ('Impresion', 'Impresion'), ('Acabado final', 'Acabado final'), ('Entregado', 'Entregado')], max_length=125, verbose_name='Nombre')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fases', to='ventas.cliente', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Fase',
                'verbose_name_plural': 'Fases',
                'db_table': 'fase',
            },
        ),
    ]
