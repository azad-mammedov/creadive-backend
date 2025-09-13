from django import forms

from .models import TeamMember, SocialLink, ServiceFeature


class TeamMemberForm(forms.ModelForm):
    """Form for TeamMember model - social links are handled via inline admin"""
    class Meta:
        model = TeamMember
        fields = "__all__"


class SocialLinkForm(forms.ModelForm):
    """Form for SocialLink model"""
    class Meta:
        model = SocialLink
        fields = "__all__"


class ServiceFeatureForm(forms.ModelForm):
    """Form for ServiceFeature model"""
    class Meta:
        model = ServiceFeature
        fields = "__all__"
