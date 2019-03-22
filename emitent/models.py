from django.db import models
from django.conf import settings
from model_utils import Choices
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from django.utils.translation import gettext as _


#
#  Decorator to add admin settings
#
def admin_method_attributes(**outer_kwargs):
    """ Wrap an admin method with passed arguments as attributes and values.
    DRY way of extremely common admin manipulation such as setting short_description, allow_tags, etc.
    """

    def method_decorator(func):
        for kw, arg in outer_kwargs.items():
            setattr(func, kw, arg)
        return func

    return method_decorator


class Emitent(models.Model):
    """
    Emitent model.
    Provide all nessesary information for one emitent published on MOEX.
    Available info:
        Text fields includes name, features, additional info about company and industry info
        Technical fields includes multiplications, current prices, etc
        Admin fields includes information for admin views and publishing

    """
    #  Choices for publishing stages
    WORK_STATE_CHOICES = Choices((0, 'empty', 'Empty'),
                                 (1, 'working', 'Working'),
                                 (2, 'verification', 'Waiting verification'),
                                 (3, 'publish', 'Ready to publish'))

    #
    # -----Base information fields-----
    #

    # Name
    name = models.CharField(max_length=100,
                            null=True,
                            verbose_name='Emitent name')

    # Industry
    industry = models.ForeignKey(
        to='Industry',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Emitent industry group'
    )

    # Industry sub-group
    industry_subgroup = models.ForeignKey(
        to='IndustrySubgroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    # Main page
    web_site = models.URLField(
        null=True,
        blank=True,
        verbose_name='Web site')

    # Documents page (economical)
    documents_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Documents url')

    #
    # -----Text fields-----
    #

    #  Main positive features
    main_advantages = models.TextField(
        null=True,
        blank=True,
        verbose_name='Emitent positive features'
    )

    #  Main negative features
    main_disadvantages = models.TextField(
        null=True,
        blank=True,
        verbose_name='Emitent negative features'
    )

    # Short history
    short_history = models.TextField(
        null=True,
        blank=True,
        verbose_name='Short history'
    )

    # Additional information, features, traits, news, etc
    additional_info = models.TextField(
        null=True,
        blank=True,
        verbose_name='Additional information'
    )

    #
    # -----Admin fields-----
    #

    # Publish state based on Choices
    publish_stage = models.IntegerField(
        choices=WORK_STATE_CHOICES,
        default=WORK_STATE_CHOICES.empty,
        verbose_name='Publish state'
    )

    # Last time the data changes, based on server time
    last_changes_time = models.DateTimeField(
        null=True,
        verbose_name='Changes date'
    )

    # Last editor changing data (registered user)
    last_editor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='User'
    )

    #
    # -----Admin/return methods-----
    #

    # Return name
    @admin_method_attributes(short_description='Company name')
    def emitent_name(self):  # Возвращает имя
        return self.name

    # Return publish status
    @admin_method_attributes(short_description='Publish state')
    def emitent_publish_status(self):  # Возвращает готовность редактированмя
        return self.WORK_STATE_CHOICES.__getitem__(self.publish_stage)

    # Return last edit time
    @admin_method_attributes(short_description='Last changes')
    def emitent_admin_last_edit_time(self):  # Возвращает время редактирования
        return self.last_changes_time

    # Return last editor name (user)
    @admin_method_attributes(short_description='User')
    def emitent_last_editor(self):  # Возвращает имя пользователя, внесшего изменения
        return self.last_editor

    #
    # -----Overrides-----
    #

    #  Validation during clean method, check some sensitive fields
    def clean(self):

        if self.industry is not None and self.industry_subgroup is not None:
            try:
                #  Try to find subindustry in industry group by get() method
                IndustrySubgroup.objects.get(industry=self.industry, subgroup=self.industry_subgroup)
            except ObjectDoesNotExist:
                #  If not, raise Validation error and messaging user
                raise ValidationError(
                    _('Sub-industry %(sub)s is not related to %(ind)s industry group'),
                    code='emitent invalid subgroup relation',
                    params={'sub': self.industry_subgroup,
                            'ind': self.industry},
                )

        elif self.industry_subgroup is not None:

            #  If get subindustry without industry, raise Validation error
            raise ValidationError(
                _('Need to choose industry, to provide sub-industry'),
                code='emitent no industry',
                params={},
            )

        #  Get edit time
        self.last_changes_time = timezone.now()


class Industry(models.Model):
    """
    Model of industry sector
    Provide minimal text information about industry sector
    """

    #  Choices for publishing stages
    WORK_STATE_CHOICES = Choices((0, 'empty', 'Empty'),
                                 (1, 'working', 'Working'),
                                 (2, 'verification', 'Waiting verification'),
                                 (3, 'publish', 'Ready to publish'))

    # name
    industry = models.CharField(unique=True, max_length=100)

    # url in system
    url_name = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        verbose_name='url short'
    )

    # minimal text information about industry sector
    short_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='short description'
    )

    #  publish stage for admin and users
    publish_stage = models.IntegerField(
        choices=WORK_STATE_CHOICES,
        default=WORK_STATE_CHOICES.empty,
        verbose_name='Publish state'
    )

    #
    # -----Admin methods-----
    #

    # Return name
    @admin_method_attributes(short_description='Industry')
    def industry_name_return(self):
        return self.industry

    # Return publish stage
    @admin_method_attributes(short_description='Publish state')
    def publish(self):
        return self.WORK_STATE_CHOICES.__getitem__(self.publish_stage)

    #
    # -----Overrides----
    #

    # return name
    def __str__(self):
        return self.industry


class IndustrySubgroup(models.Model):
    """
    Sub-industry sector model
    Provide minimal text information about sub-sector
    """

    #  Choices for publishing stages
    WORK_STATE_CHOICES = Choices((0, 'empty', 'Empty'),
                                 (1, 'working', 'Working'),
                                 (2, 'verification', 'Waiting verification'),
                                 (3, 'publish', 'Ready to publish'))

    # Foreign related field to industry model
    industry = models.ForeignKey(
        to='Industry',
        to_field='industry',
        on_delete=models.CASCADE,
        related_name='industry_name'
    )

    # name
    subgroup = models.CharField(
        null=True,
        unique=True,
        blank=True,
        max_length=100
    )

    # url
    url_name = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        verbose_name='url short',
        null=True
    )

    # minimal text information about industry sector
    short_description = models.TextField(
        null=True,
        blank=True,
        verbose_name='short description',
    )

    # publish stages
    publish_stage = models.IntegerField(
        choices=WORK_STATE_CHOICES,
        default=WORK_STATE_CHOICES.empty,
        verbose_name='Publish state'
    )

    #
    # -----Admin methods----
    #

    # return foreign related industry name
    @admin_method_attributes(short_description='Industry')
    def industry_name_return(self):
        return self.industry

    # return name
    @admin_method_attributes(short_description='Sub-industry')
    def sub_industry_name(self):
        return self.subgroup

    # return publish stage
    @admin_method_attributes(short_description='Publish state')
    def publish(self):
        return self.WORK_STATE_CHOICES.__getitem__(self.publish_stage)

    #
    # -----Overrides----
    #

    # return name
    def __str__(self):
        return self.subgroup
