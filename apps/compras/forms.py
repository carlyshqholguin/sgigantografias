from django import forms
from .models import Compra, DetalleCompra,Insumo,Proveedor



class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: left;width: 100%;margin: 0px;'

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'inventario', 'factura']
        exclude = ['impuesto_iva','impuesto_it']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: left;width: 100%;margin: 0px;'

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['insumo', 'cantidad']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'text-align: left;width: 100%;margin: 0px;'

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['proveedor', 'nombre', 'detalle', 'categoria', 'precio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control '
            field.widget.attrs['style'] = 'text-align: left; width: 100% !important; margin: 0px; padding: 5px;'



