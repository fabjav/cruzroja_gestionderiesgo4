from django import forms
from .models import Casa, Barrio, Persona

class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = ['nombre', 'calle', 'numero', 'barrio']

class BarrioForm(forms.ModelForm):
    class Meta:
        model = Barrio
        fields = ['nombre', 'coordenadas', 'distrito']

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'foto_perfil', 'casa', 'primario', 'secundario',
                  'terciario', 'padecimientos', 'medicamento', 'dosis', 'telefono_emergencia', 'fecha_nac', 'dni', 'rol']
