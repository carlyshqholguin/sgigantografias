# Generated by Django 4.2.9 on 2024-02-04 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_alter_resultadoanalisis_options_and_more'),
    ]

    operations = [
        #migrations.RemoveField(
        #    model_name='fase',
        #    name='nombre',
        #),
        #migrations.RemoveField(
        #    model_name='resultadoanalisis',
        #    name='created_at',
        #),
        #migrations.RemoveField(
        #    model_name='venta',
        #    name='analizada',
        #),
        migrations.AddField(
            model_name='fase',
            name='fase',
            field=models.CharField(blank=True, choices=[('Pendiente', 'Pendiente'), ('Rayado y corte', 'Rayado y corte'), ('Impresion', 'Impresion'), ('Acabado final', 'Acabado final'), ('Entregado', 'Entregado')], max_length=125, null=True, verbose_name='Fase'),
        ),
    ]
