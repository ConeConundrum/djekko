from django.test import TestCase
from emitent.models import Emitent, Industry, IndustrySubgroup
from django.db.utils import IntegrityError as IntegrityErrorDjango
from psycopg2 import IntegrityError as IntegrityErrorPostgres


def create_emitent_model(name, industry=None, industry_subgroup=None):
    emitent_entry = Emitent.objects.create(name=name,
                                           industry=industry,
                                           industry_subgroup=industry_subgroup,
                                           web_site='http://just_a_fake_for_test',
                                           documents_url='http://just_a_fake_for_test/documents',
                                           main_advantages='Nothing good',
                                           main_disadvantages='Nothing bad',
                                           short_history='Long time ago...',
                                           additional_info='Just eggs',
                                           publish_stage=0,
                                           last_changes_time=None,
                                           last_editor=None)
    return emitent_entry


def create_industry_model(name):
    industry_entry = Industry.objects.create(
        industry=name,
        url_name=name + '_t',
        short_description='nothing interesting',
        publish_stage=0)
    return industry_entry


def create_industry_subgroup_model(name, industry=None):
    sub_industry_entry = IndustrySubgroup.objects.create(industry=industry,
                                                         subgroup=name,
                                                         url_name=name + '_st',
                                                         short_description='Nothing special',
                                                         publish_stage=0)
    return sub_industry_entry


class EmitentAppModelTest(TestCase):
    emitent_entry_1 = None
    emitent_entry_2 = None
    industry_entry_1 = None
    industry_entry_2 = None
    sub_industry_entry_1 = None
    sub_industry_entry_2 = None

    def setUp(self):

        self.emitent_entry_1 = create_emitent_model(name='Gazprom')
        self.emitent_entry_2 = create_emitent_model(name='NeftGaz')
        self.industry_entry_1 = create_industry_model(name='Oil')
        self.industry_entry_2 = create_industry_model(name='Gaz')
        self.sub_industry_entry_1 = create_industry_subgroup_model(name='Clean Oil', industry=self.industry_entry_1)
        self.sub_industry_entry_2 = create_industry_subgroup_model(name='Clean gaz', industry=self.industry_entry_2)

        self.assertTrue(isinstance(self.emitent_entry_1, Emitent))
        self.assertTrue(isinstance(self.emitent_entry_2, Emitent))
        self.assertTrue(isinstance(self.industry_entry_1, Industry))
        self.assertTrue(isinstance(self.industry_entry_2, Industry))
        self.assertTrue(isinstance(self.sub_industry_entry_1, IndustrySubgroup))
        self.assertTrue(isinstance(self.sub_industry_entry_2, IndustrySubgroup))

    def test_emitent_unique_creation(self, ):
        try:
            create_emitent_model('Gazprom')
            self.fail('Integrity error, two unique objects was created')
        except (IntegrityErrorDjango, IntegrityErrorPostgres):
            pass

    def test_industry_unique_creation(self):

        try:
            create_industry_model(name='Oil')
            self.fail('Integrity error, two unique objects was created')
        except (IntegrityErrorDjango, IntegrityErrorPostgres):
            pass

    def test_sub_industry_unique_creation(self):

        try:
            create_industry_subgroup_model(name='Clean Oil', industry=self.industry_entry_1)
            self.fail('Integrity error, two unique objects was created')
        except (IntegrityErrorDjango, IntegrityErrorPostgres):
            pass
