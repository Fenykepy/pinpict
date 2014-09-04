from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from user.models import User
from board.slug import unique_slugify


BOARD_POLICY_CHOICES = (
            (0, 'Private'),
            (1, 'Public'),
        )



class PublicBoardsManager(models.Manager):
    """Returns a queryset with all public boards."""
    def get_query_set(self):
        return super(PublicBoardsManager, self).get_query_set().filter(
                policy=1)




class PrivateBoardsManager(models.Manager):
    """Returns a queryset with all public boards."""
    def get_query_set(self):
        return super(PrivateBoardsManager, self).get_query_set().filter(
                policy=0)



class Board(models.Model):
    """Table for all boards."""
    date_created = models.DateTimeField(auto_now_add=True,
            auto_now=False,
            verbose_name="Creation date")
    date_updated =models.DateTimeField(auto_now_add=True,
            auto_now=True,
            verbose_name="Last update date")
    title = models.CharField(max_length=254, verbose_name="Title")
    slug = models.SlugField(max_length=254, db_index=True,
            verbose_name="Slug")
    description = models.TextField(null=True, blank=True,
            verbose_name="Board description")
    n_pins = models.PositiveIntegerField(default=0,
            verbose_name="Pins number")
    policy = models.PositiveIntegerField(
            choices=BOARD_POLICY_CHOICES, verbose_name="Policy")
    user = models.ForeignKey(User)
    order = models.PositiveIntegerField(default=100000)

    # managers
    objects = models.Manager()
    publics = PublicBoardsManager()
    privates = PrivateBoardsManager()

    class Meta:
        ordering = ['order', 'date_created']
        unique_together = (('user', 'slug'),)

    def save(self, **kwargs):
        """Make a unique slug for from title, then save."""
        slug = '%s' % (self.title)
        unique_slugify(self, slug,
                queryset=Board.objects.filter(user=self.user))
        super(Board, self).save()

    def __str__(self):
        return "%s" % self.title

@receiver(post_save, sender=Board)
@receiver(post_delete, sender=Board)
def update_user_n_boards(sender, instance, **kwargs):
    """Update user's n_boards after board save or delete."""
    instance.user.n_boards = Board.objects.filter(user = instance.user).count()
    instance.user.save()


