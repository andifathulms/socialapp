from django import forms
from django.conf import settings

from .models import UserProfile

class ProfileUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = UserProfile
        fields = ('fullname', 'bio', 'phone', 'hobby','birth_date', 'birth_place', 'location', 'accWebsite',
        'accGithub', 'accTwitter', 'accInsta', 'accFacebook', 'schoolSD', 'schoolSMP', 'schoolSMA',
        'nobp', 'occupation', 'jurusan' )

    """ add to filter
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)"""

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        profile.fullname = self.cleaned_data['fullname']
        profile.bio = self.cleaned_data['bio']
        profile.phone = self.cleaned_data['phone']
        profile.hobby = self.cleaned_data['hobby']
        profile.birth_date = self.cleaned_data['birth_date']
        profile.birth_place = self.cleaned_data['birth_place']
        profile.location = self.cleaned_data['location']
        profile.accWebsite = self.cleaned_data['accWebsite']
        profile.accGithub = self.cleaned_data['accGithub']
        profile.accTwitter = self.cleaned_data['accTwitter']
        profile.accInsta = self.cleaned_data['accInsta']
        profile.accFacebook = self.cleaned_data['accFacebook']
        profile.schoolSD = self.cleaned_data['schoolSD']
        profile.schoolSMP = self.cleaned_data['schoolSMP']
        profile.schoolSMA = self.cleaned_data['schoolSMA']
        profile.nobp = self.cleaned_data['nobp']
        profile.occupation = self.cleaned_data['occupation']
        profile.jurusan = self.cleaned_data['jurusan']

        if commit:
            profile.save()
        return profile