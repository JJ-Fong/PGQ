from django import forms 
from . import form_filler 

class POSForm(forms.Form): 
	class Meta:
		pos_cod = forms.CharField(label="POS:", widget=forms.Select(choices=form_filler.pos_codes()))
		#fct_date = forms.CharField(label="Date:", widget=forms.Select(choices=form_filler.available_date()))


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['pos_cod'] = forms.CharField(label="POS:", widget=forms.Select(choices=form_filler.pos_codes(1)))
		self.fields['pos_cod'].widget.attrs.update({'class': 'custom-select'})
		#self.fields['fct_date'] = forms.CharField(label="Date:", widget=forms.Select(choices=form_filler.available_date(1)))
		#self.fields['fct_date'].widget.attrs.update({'class': 'custom-select'})
