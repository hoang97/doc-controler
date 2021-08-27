from django import forms
from .models import XFile

class XFileCreateForm(forms.ModelForm):
    
    class Meta:
        model = XFile
        fields = ['code', 'description', 'type', 'editors', 'checkers', 'approvers', 'targets']

class XFileUpdateForm(forms.ModelForm):

    class Meta:
        model = XFile
        fields = ['code', 'description', 'targets', 'content', 'department']