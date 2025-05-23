from django.forms import ModelForm, DateTimeInput
from django.contrib.auth.forms import UserCreationForm
from workmates.models import workmateUser
from tasks.models import InventoryItem, TaskProfile

class WorkmateUserCreationForm(UserCreationForm):
    class Meta:
        model = workmateUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DateInput(DateTimeInput):
    input_type = 'date'

class InventoryItemForm(ModelForm):
    class Meta:
        model = InventoryItem
        fields = ('name', 'description', 'quantity', 'expiry_date', 'item_type', 'added_by')
        widgets = {
            'expiry_date': DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        item = super().save(commit=False)
        if commit:
            item.save()
        return item
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control form-control-sm w-50'})
    
     
        self.fields['name'].widget.attrs.update({
            'style': 'width: 100%; height: 40px;',  # Más ancho y menor altura
        })
        self.fields['description'].widget.attrs.update({
            'rows': 2,  # Reduce el número de filas para hacerlo horizontal
            'style': 'width: 100%; resize: none;',  # Evita el redimensionamiento
        })
    
class WorkmateTaskAssign(ModelForm):
    class Meta:
        model = TaskProfile
        fields = ('user', 'task')

    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
        return task
