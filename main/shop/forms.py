from django import forms

from shop.models import CharName, ProductChar

class ProductFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        char_names = CharName.objects.filter(filter_add=True)
        for char_name in char_names:
            values = ProductChar.objects.filter(char_name=char_name).values_list('char_value', flat=True).distinct()
            self.fields[char_name.filter_name] = forms.MultipleChoiceField(
                choices=[(value, value) for value in values],
                widget=forms.CheckboxSelectMultiple(
                    attrs={'class': 'form__controls-checkbox filter-checkbox'}
                ),
                required=False,
                label=char_name.text_name
            )