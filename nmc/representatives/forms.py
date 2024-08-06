from django import forms
from .models import Representative, County, Ward


class RepresentativeForm(forms.ModelForm):
    class Meta:
        model = Representative
        fields = ['photo', 'name', 'id_number', 'phone_number', 'ward', 'position']

    county = forms.ModelChoiceField(queryset=County.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'county' in self.data:
            try:
                county_id = int(self.data.get('county'))
                self.fields['ward'].queryset = Ward.objects.filter(county_id=county_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty Ward queryset
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.county.wards.order_by('name')
        else:
            self.fields['ward'].queryset = Ward.objects.none()


class CountyForm(forms.ModelForm):
    class Meta:
        model = County
        fields = ['name']


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['name']
