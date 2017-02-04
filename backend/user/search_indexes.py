from haystack import indexes
from user.models import User

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    last_name = indexes.CharField(model_attr='last_name')
    first_name = indexes.CharField(model_attr='first_name')
    username = indexes.CharField(model_attr='username')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

