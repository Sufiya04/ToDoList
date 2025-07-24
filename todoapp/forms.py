from typing import Any
from django import forms
class TodoList(forms.Form):
    task=forms.CharField(max_length=50)
    des=forms.CharField(max_length=100)
    # time=forms.TimeField()
    def clean(self) -> dict[str, Any]:
        cleaned_data=super().clean()
        mytask=self.cleaned_data['task']
        descript=self.cleaned_data['des']
        if mytask.isupper():
            self.add_error('task','Use Lower')
        if descript.isupper():
            self.add_error('des','Use Lower')
        print(cleaned_data)
        return self.cleaned_data
