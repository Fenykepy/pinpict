import os
import io

from wand.image import Image

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from board.slug import unique_slugify
from pinpict.settings import AVATAR_MAX_SIZE, MEDIA_ROOT
from pin.utils import get_sha1_hexdigest
from pinpict.settings import DEFAULT_FROM_EMAIL

from thumbnail import ThumbnailFactory


def has_changed(instance, field, manager='objects'):
    """Returns true if a field has changed in a model

    May be used in a model.save() method.

    """
    if not instance.pk:
        return True
    manager = getattr(instance.__class__, manager)
    old = getattr(manager.get(pk=instance.pk), field)
    return not getattr(instance, field) == old
    


class Notification(models.Model):
    """Table for all notifications."""
    date = models.DateTimeField(auto_now_add=True, db_index=True,
            auto_now=False,
            verbose_name="Creation date")
    type = models.CharField(max_length=254, null=True, blank=True)
    title = models.TextField(null=True, blank=True,
            verbose_name="Title")
    read = models.BooleanField(default=False, db_index=True)
    receiver = models.ForeignKey('User', related_name="receiver", null=True)
    sender = models.ForeignKey('User', related_name="sender", null=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-date']


    def save(self, **kwargs):
        """Increment user unread_notifications number and send mails
        if necessary."""
        # if notification is created
        if self.pk == None:
            # increment user unread notifications number
            self.receiver.n_unread_notifications += 1
            self.receiver.save()

            # send mail if necessairy
            if self.sender.root_uri:
                root_uri = self.sender.root_uri
            else:
                root_uri = ''
            sender_url = root_uri + reverse('boards_list', kwargs={
                'user': self.sender.slug,
            })
            subject = False
            if (self.receiver.mail_user_follower and 
                    self.type == "USER_FOLLOWER"):
                subject = "{} started to follow you".format(
                        self.sender.username)
                message = ("{}!\n"
                    "see his profile:\n"
                    "{}\n\n"
                ).format(
                    subject,
                    sender_url,
                )
            elif (self.receiver.mail_board_follower and
                    self.type =="BOARD_FOLLOWER"):
                subject = "{} started to follow your board {}".format(
                        self.sender.username,
                        self.content_object.title)
                message = ("{}!\n"
                        "see his profile:\n"
                        "{}\n"
                        "see board:\n"
                        "{}\n\n"
                ).format(
                    subject,
                    sender_url,
                    root_uri + reverse('board_view', kwargs={
                            'user': self.sender.slug,
                            'board': self.content_object.slug,
                    }),
                )
            elif (self.receiver.mail_following_add_pin and
                    self.type == "ADD_PIN"):
                subject = "{} added a pin on board {}".format(
                        self.sender.username,
                        self.content_object.board.title)
                message = ("{}!\n"
                        "See pin:\n"
                        "{}\n\n"
                ).format(
                    subject,
                    root_uri + reverse('pin_view', kwargs={
                        'pk': self.content_object.pk,
                    }),
                )
            elif (self.receiver.mail_following_add_board and
                    self.type == "ADD_BOARD"):
                subject = "{} added a new board {}".format(
                        self.sender.username,
                        self.content_object.title)
                message = ("{}!\n"
                        "See board:\n"
                        "{}\n\n"
                ).format(
                    subject,
                    root_uri + reverse('board_view', kwargs={
                            'user': self.sender.slug,
                            'board': self.content_object.slug,
                    }),
                )

            elif (self.receiver.mail_repinned and
                    self.type == "RE_PINNED"):
                subject = "{} pinned one of your pins".format(
                        self.sender.username)
                message = ("{}!\n"
                        "See new pin:\n"
                        "{}\n\n"
                ).format(
                    subject,
                    root_uri + reverse('pin_view', kwargs={
                        'pk': self.content_object.pk,
                    }),
                )

            elif (self.receiver.mail_allow_read and
                    self.type == "ALLOW_READ"):
                subject = "{} allowed you to see his private board {}".format(
                        self.sender.username,
                        self.content_object.title)
                message = ("{}!\n"
                        "See board:\n"
                        "{}\n\n"
                ).format(
                    subject,
                    root_uri + reverse('board_view', kwargs={
                            'user': self.sender.slug,
                            'board': self.content_object.slug,
                    }),
                )



            if subject:
                lead = ("Hi {}! \n\n").format(self.receiver.username)
                trail = ("\n##########################################\n\n"
                           "Don't want to see this mail ? unsuscribe :\n{}\n"
                ).format(
                        root_uri + reverse('user_profil')
                )
                message = lead + message + trail
                self.receiver.send_mail(subject, message)


        # save object
        super(Notification, self).save()



class User(AbstractUser):
    """User extention table."""
    slug = models.SlugField(max_length=30, db_index=True,
                unique=True, verbose_name="Slug")
    uuid = models.CharField(max_length=42, blank=True, null=True)
    uuid_expiration = models.DateTimeField(blank=True, null=True)
    root_uri = models.URLField(blank=True, null=True,
            verbose_name="Home page URI, without trailing slash")
    avatar = models.ImageField(
            null=True, blank=True,
            upload_to='images/avatars',
            verbose_name="Avatar",
            help_text="A picture to download as avatar."
    )
    website = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="Site web",
            help_text="A link to your website."
    )
    facebook_link = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="Facebook",
            help_text="A link to your facebook page."
    )
    flickr_link = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="Flickr",
            help_text="A link to your flickr page."
    )
    px500_link = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="500px",
            help_text="A link to your 500px page."
    )
    twitter_link = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="Twitter",
            help_text="A link to your twitter page."
    )
    gplus_link = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="Google +",
            help_text="A link to your google + page."
    )
    pinterest_link = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="Pinterest",
            help_text="A link to your pinterest page."
    )
    vk_link = models.URLField(
            null=True,
            blank=True,
            max_length=2000,
            verbose_name="Vkontakte",
            help_text="A link to your vkontakte page."
    )
    followers = models.ManyToManyField("self", null=True, blank=True,
            symmetrical=False,
            related_name="following",
            verbose_name="Users who follow user")
    n_followers = models.PositiveIntegerField(default=0,
            verbose_name="Followers number")
    n_following = models.PositiveIntegerField(default=0,
            verbose_name="Followed users number")
    n_public_pins = models.PositiveIntegerField(default=0,
            verbose_name="Public pins'number")
    n_pins = models.PositiveIntegerField(default=0,
            verbose_name="Pins'number")
    n_boards = models.PositiveIntegerField(default=0,
            verbose_name="Boards'number")
    n_public_boards = models.PositiveIntegerField(default=0,
            verbose_name="Public Boards'number")
    n_unread_notifications = models.PositiveIntegerField(default=0,
            verbose_name="New notifications")
    mail_user_follower = models.BooleanField(default=True,
         verbose_name="Receive a mail when a user starts to follow me")
    mail_board_follower = models.BooleanField(default=True,
    verbose_name=("Receive a mail when a user starts to follow"
        " one of my boards"))
    mail_following_add_pin = models.BooleanField(default=True,
    verbose_name="Receive a mail when following user add a new pin")
    mail_following_add_board = models.BooleanField(default=True,
    verbose_name="Receive a mail when following user add a new board")
    mail_repinned = models.BooleanField(default=True,
    verbose_name="Receive a mail when one of my pins are pinned")
    mail_allow_read = models.BooleanField(default=True,
    verbose_name=("Receive a mail when a user allows me to see one"
        " of it's private boards"))

    
    def set_n_followers(self):
        """Set number of followers."""
        self.n_followers = self.followers.all().count()
        self.save()

    def set_n_following(self):
        """Set number of followed users."""
        print('set_n_following')
        print(self.username)
        self.n_following = self.following.all().count()
        self.save()
    

    def add_follower(self, follower):
        """Add a follower to the user.
        follower: user object."""
        self.followers.add(follower)
        self.set_n_followers()
        follower.set_n_following()
        for board in self.board_set.all():
            board.add_follower(follower, notification=False)

        # send notification
        Notification.objects.create(
            type="USER_FOLLOWER",
            sender=follower,
            receiver=self,
            title="started to follow you.",
            content_object=follower
        )





    def remove_follower(self, follower):
        """Remove a follower to the user.
        follower: user object."""
        self.followers.remove(follower)
        self.set_n_followers()
        follower.set_n_following()
        for board in self.board_set.all():
            board.remove_follower(follower)


    def get_public_boards(self):
        return self.board_set.filter(policy=1)


    def get_notifications(self):
        return self.receiver.all()


    def get_unread_notifications(self):
        return self.receiver.filter(read=False)


    def set_notifications_read(self):
        self.get_unread_notifications().update(read=True)


    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.username


    def get_full_name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        return self.get_short_name()


    def send_mail(self, subject, message):
        """send a mail to user."""
        return send_mail(
                subject,
                message,
                DEFAULT_FROM_EMAIL,
                [self.email],
        )
    
    def get_pins(self):
        """return a queryset with all user's pin."""
        return self.pin_user.all()

    def get_public_pins(self):
        """return a queryset with all user's public pins."""
        return self.pin_user.filter(policy=1)

    def get_n_pins(self):
        """get user n_pins."""
        return self.get_pins().count()

    def get_n_public_pins(self):
        """get user n_public_pins."""
        return self.get_public_pins().count()

    def get_n_boards(self):
        """get user n_boards."""
        return self.board_set.all().count()

    def get_n_public_boards(self):
        return self.board_set.filter(policy=1).count()

    def get_absolute_url(self):
        return reverse('boards_list', kwargs={
            'user': self.slug})

    def save(self, **kwargs):
        """Make a unique slug from username then save."""
        if self.pk == None:
            slug = '%s' % (self.username)
            unique_slugify(self, slug)


        if self.avatar and has_changed(self, 'avatar'):
            with ThumbnailFactory(file=self.avatar.file) as img:
                img.resize_crop(AVATAR_MAX_SIZE, AVATAR_MAX_SIZE)
                format = img.img.format
                temp = io.BytesIO()
                img.save(stream=temp)
                temp.seek(0)
            uploaded_file = SimpleUploadedFile('temp', temp.read())
            # set filename
            filename = '{}.{}'.format(self.id, format.lower())
            # save avatar
            self.avatar.save(
                    filename,
                    uploaded_file,
                    save=False)

        # save object
        super(User, self).save()



def mail_superusers(subject, message):
    """Send a mail to all super users."""
    # get superusers
    superusers = User.objects.filter(is_superuser=True)
    # get superusers' mails in a list
    superusers_mails = [superuser.email for superuser in superusers]
    # send mail to superusers
    send_mail(subject, message, DEFAULT_FROM_EMAIL, superusers_mails)



def mail_staffmembers(subject, message):
    """Send a mail to all staff members."""
    # get staff members
    staffmembers = User.objects.filter(is_staff=True)
    # if no staff member, send mail to super user
    if not staffmembers:
        print('No staff members found, send mail to superusers.')
        return mail_superusers(subject, message)

    # get staff members' mails in a list
    staffmembers_mails = [staffmember.email for staffmember in staffmembers]
    # send mail to staff members
    send_mail(subject, message, DEFAULT_FROM_EMAIL, staffmembers_mails)

