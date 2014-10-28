import os
import io

from wand.image import Image

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

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



class User(AbstractUser):
    """User extention table."""
    slug = models.SlugField(max_length=30, db_index=True,
                unique=True, verbose_name="Slug")
    uuid = models.CharField(max_length=42, blank=True, null=True)
    uuid_expiration = models.DateTimeField(blank=True, null=True)
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

    n_public_pins = models.PositiveIntegerField(default=0,
            verbose_name="Public pins'number")
    n_pins = models.PositiveIntegerField(default=0,
            verbose_name="Pins'number")
    n_boards = models.PositiveIntegerField(default=0,
            verbose_name="Boards'number")
    n_public_boards = models.PositiveIntegerField(default=0,
            verbose_name="Public Boards'number")


    def get_public_boards(self):
        return self.board_set.filter(policy=1)


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


    
