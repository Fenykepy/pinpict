from haystack import indexes
from board.models import Board

class BoardIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Board

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().publics.all()
