from django import forms
from home.models import NewsArticle, Chatterbox, ArticleComment


class NewsArticleForm(forms.ModelForm):

    class Meta:
        model = NewsArticle
        #fields = ('title', 'body', 'pub_date', 'thumbnail')
        fields = ('title', 'body', 'thumbnail')

    #Rename 'thumbnail' to 'image'
    def __init__(self, *args, **kwargs):
        super(NewsArticleForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].label = "Image"


class CommentForm(forms.ModelForm):

    class Meta:
        model = ArticleComment
        fields = ('body',)


class DeleteNewsArticleForm(forms.ModelForm):

    class Meta:
        model = NewsArticle
        fields = []


class DeleteCommentForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = []


class ChatterboxForm(forms.ModelForm):

    class Meta:
        model = Chatterbox
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Write something'})
        }


class ChatterboxDeleteForm(forms.ModelForm):

    class Meta:
        model = NewsArticle
        fields = []