from django import forms

from app.models import Band, Listing

class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        #fields = '__all__'
        exclude = ('active', 'official_homepage')

class ListForm(forms.ModelForm):
    class Meta:
        model = Listing
        #fields = '__all__'
        exclude = ('sold', 'year')