from django import forms
from .models import Venta,Cliente,Cotizacion,Fase

class VentaForm(forms.ModelForm):
    
    class Meta:
        model = Venta
        fields = ['cliente', 'tipo', 'inventario', 'costo_impresion', 'costo_trabajo', 'factura', 'insumos']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: left;width: 100%;margin: 0px;'


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: left;width: 100%;margin: 0px;'


class FaseForm(forms.ModelForm):
    class Meta:
        model = Fase
        fields = '__all__'  # Puedes especificar los campos que deseas mostrar en el formulario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: left; width: 100%; margin: 0px;'