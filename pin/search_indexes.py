from haystack import indexes
from pin.models import Pin

class PinIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='pin_user')
    #description = indexes.CharField(model_attr='description')

    def get_model(self):
        return Pin

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(policy=1)

