from django import forms
from django.core.management import call_command

from parse_m2.models import Metro2Event

import os


class Metro2EventForm(forms.ModelForm):
    class Meta:
        model = Metro2Event
        fields = ['name',]
        help_texts = {'name': "Provide an event name"}
    directory = forms.CharField(label="Data Directory", max_length=300, required=False)
    enabled = os.environ.get("S3_ENABLED")
    def __init__(self, *args, **kwargs):
        super(Metro2EventForm, self).__init__(*args, **kwargs)

        if self.enabled:
            self.fields['directory'].label = 'S3 Bucket'
            self.fields['directory'].help_text = 'Provide the bucket name where the data files are located'
        else:
            self.fields['directory'].label = 'Data Directory'
            self.fields['directory'].help_text = 'Provide the directory where the data files are located'

    def save_m2m(self):
        pass
    def save(self, commit):
        # This is called only when it is for a new Metro2Event
        if self.is_valid() & self.has_changed():
            super(Metro2EventForm, self).save(commit=False)
            self.save_m2m()
            event_name = self.cleaned_data["name"]
            directory = self.cleaned_data["directory"]
            if self.enabled:
                call_command('parse_evaluate_s3', event_name=event_name, data_directory=directory)
            else:
                call_command('parse_local', event_name=event_name,
                            data_directory=directory)
            # The mgmt command saves the Metro2Event, so we need to retrieve the
            # most recently saved Metro2Event object by name
            return Metro2Event.objects.latest('name')
        else:
            return self.instance
