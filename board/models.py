from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from pinpict.settings import BOARD_RESERVED_WORDS
from user.models import User, has_changed, Notification
from board.slug import unique_slugify


BOARD_POLICY_CHOICES = (
        (0, 'Private'),
        (1, 'Public'),
)

PIN_ORDERING_CHOICES = (
        ('date_created', 'Date'),
        ('owner_rate', 'Rating'),
        ('source_domain', 'Domain pin comes from'),
)




class PublicBoardsManager(models.Manager):
    """Returns a queryset with all public boards."""
    def get_queryset(self):
        return super(PublicBoardsManager, self).get_queryset().filter(
                policy=1)




class PrivateBoardsManager(models.Manager):
    """Returns a queryset with all public boards."""
    def get_queryset(self):
        return super(PrivateBoardsManager, self).get_queryset().filter(
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
    pin_default_description = models.TextField(null=True, blank=True,
            verbose_name="Default description",
            help_text=("Pin default description used if pinned image "
                "has no alt attribute."))
    n_pins = models.PositiveIntegerField(default=0,
            verbose_name="Pins number")
    policy = models.PositiveIntegerField(
            choices=BOARD_POLICY_CHOICES, verbose_name="Policy",
            null=False, blank=False, default=1)
    user = models.ForeignKey(User)
    order = models.PositiveIntegerField(default=100000)
    pins_order = models.CharField(max_length=254, null=True, blank=True,
            choices=PIN_ORDERING_CHOICES, default='date_created',
            verbose_name="Order pins by")
    reverse_pins_order = models.BooleanField(default=False,
            verbose_name="Descending order")
    users_can_read = models.ManyToManyField(User, null=True, blank=True,
            related_name="users_can_read",
            verbose_name="Users who can see board if private")
    followers = models.ManyToManyField(User, null=True, blank=True,
            related_name="board_followers",
            verbose_name="Users who follow board")
    n_followers = models.PositiveIntegerField(default=0,
            verbose_name="Followers number")

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
        # ensure reserved words are not used as board slug:
        if slug in BOARD_RESERVED_WORDS:
            slug = slug + '-1'
        unique_slugify(self, slug,
                queryset=Board.objects.filter(user=self.user))

        # if policy has changed, update pin's policy
        if has_changed(self, 'policy'):
            self.pin_set.all().update(policy=self.policy)
            self.user.n_public_pins = self.user.get_n_public_pins()
            self.user.n_public_boards = self.user.get_n_public_boards()
            self.user.save()


        # save object
        super(Board, self).save()

    def get_absolute_url(self):
        return reverse('board_view', kwargs={
            'user': self.user.slug,
            'board': self.slug,
        })

    def get_sorted_pins(self):
        """Return board's pins sorted by "pins_order" field and
        reverse if reverse_pins_order."""
        prefix = ''
        if self.reverse_pins_order:
            prefix = '-'
        return self.pin_set.all().order_by(prefix + self.pins_order)

    def get_main_cover(self):
        """Return main cover pin instance."""
        mains = self.pin_set.all().filter(main=True);
        # try to get main pin else return first one if any
        try:
            main = mains.get()
            return main
        except:
            return self.pin_set.all()[:1].get()

    def set_n_followers(self):
        """Set number of followers."""
        self.n_followers = self.followers.all().count()
        self.save()

    def add_follower(self, follower, notification=True):
        """Add a follower to the board.
        follower: user object."""
        self.followers.add(follower)
        self.set_n_followers()
        if not notification:
            return
        # else send notification
        Notification.objects.create(
            type="BOARD_FOLLOWER",
            sender=follower,
            receiver=self.user,
            title="suscribed to your board",
            content_object=self
        )


    def remove_follower(self, follower):
        """Remove a follower from thes board.
        follower: user object."""
        self.followers.remove(follower)
        self.set_n_followers()

    def __str__(self):
        return "%s" % self.title



@receiver(post_save, sender=Board)
@receiver(post_delete, sender=Board)
def update_user_n_boards(sender, instance, **kwargs):
    """Update user's n_boards after board save or delete."""
    instance.user.n_boards = instance.user.get_n_boards()
    instance.user.n_public_boards = instance.user.get_n_public_boards()
    instance.user.save()


@receiver(m2m_changed, sender=Board.users_can_read.through)
def allow_private_board_read(sender, instance, action, reverse,
        model, pk_set, **kwargs):
    """Send a notification when an user has been allowed
    to read a private board."""
    if action != 'post_add' or instance.policy != 0:
        return
    # get receiver of notification
    for elem in pk_set:
        receiver = User.objects.get(pk=elem)
        # send notification
        Notification.objects.create(
            type="ALLOW_READ",
            sender=instance.user,
            receiver=receiver,
            title="allowed you to see his private board",
            content_object=instance
        )
    



