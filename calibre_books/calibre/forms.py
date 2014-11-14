from django import forms
from haystack.forms import SearchForm as BaseSearchForm


class SearchForm(BaseSearchForm):

    g = forms.CharField(required=False)

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        query = self.cleaned_data.get('q')
        genre = self.cleaned_data.get('g')

        sqs = self.searchqueryset
        if query:
            sqs = sqs.auto_query(query)
        if genre:
            sqs = sqs.filter(genres=genre)

        if self.load_all:
            sqs = sqs.load_all()

        return sqs

    def clean(self):
        if not any([self.cleaned_data.get('q'), self.cleaned_data.get('g')]):
            raise forms.ValidationError('Missing parameters')
        return self.cleaned_data
