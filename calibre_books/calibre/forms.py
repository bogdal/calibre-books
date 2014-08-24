from haystack.forms import SearchForm as BaseSearchForm


class SearchForm(BaseSearchForm):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['q'].required = True
