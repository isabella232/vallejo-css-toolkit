from django import forms

from workflow.models import Verification


class VerificationDetailsForm(forms.ModelForm):

    class Meta:
        model = Verification

        fields = (
            'property_description',
        )


class VerificationOwnerForm(forms.ModelForm):

    class Meta:
        model = Verification

        fields = (
            'owner_name',
            'owner_address',
            'owner_primary_contact',
            'owner_secondary_contact'
        )
