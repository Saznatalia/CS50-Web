from django import forms

class NewPostForm(forms.Form):
    new_post = forms.CharField(label="", widget=forms.Textarea(attrs={'class': "post", 'id': "new_post"}))
