from django import forms
from home.models import NewsArticle


class NewsArticleForm(forms.ModelForm):

    class Meta:
        model = NewsArticle
        #fields = ('title', 'body', 'pub_date', 'thumbnail')
        fields = ('title', 'body', 'thumbnail')

    #Rename 'thumbnail' to 'image'
    def __init__(self, *args, **kwargs):
        super(NewsArticleForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].label = "Image"
