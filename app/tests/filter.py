from app.models import FieldsWithOptionsModel
import datetime
from django.test import TestCase
from google.appengine.api.datastore_errors import BadArgumentError, BadFilterError

class FilterTest(TestCase):
    floats = [5.3, 2.6, 9.1, 1.58]
    emails = ['app-engine@scholardocs.com', 'sharingan@uchias.com',
        'rinnengan@sage.de', 'rasengan@naruto.com']

    def setUp(self):
        for float, email in zip(FilterTest.floats, FilterTest.emails):
            model = FieldsWithOptionsModel(floating_point=float,
                                           integer=int(float), email=email,
                                           time=datetime.datetime.now().time())
            model.save()

    def test_gt(self):
        # test gt on float
        self.assertEquals([entity.floating_point for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          floating_point__gt=3.1).order_by('floating_point')],
                          [5.3, 9.1])

        # test gt on integer
        self.assertEquals([entity.integer for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          integer__gt=3).order_by('integer')],
                          [5, 9])

        # test filter on primary_key field
        self.assertEquals([entity.email for entity in \
                          FieldsWithOptionsModel.objects.filter(email__gt='as').
                          order_by('email')], ['rasengan@naruto.com',
                          'rinnengan@sage.de', 'sharingan@uchias.com', ])

    def test_lt(self):
        # test lt on float
        self.assertEquals([entity.floating_point for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          floating_point__lt=3.1).order_by('floating_point')],
                          [1.58, 2.6])

        # test lt on integer
        self.assertEquals([entity.integer for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          integer__lt=3).order_by('integer')],
                          [1, 2])

        # test filter on primary_key field
        self.assertEquals([entity.email for entity in \
                          FieldsWithOptionsModel.objects.filter(email__lt='as').
                          order_by('email')], ['app-engine@scholardocs.com', ])

    def test_gte(self):
        # test gte on float
        self.assertEquals([entity.floating_point for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          floating_point__gte=2.6).order_by('floating_point')],
                          [2.6, 5.3, 9.1])

        # test gte on integer
        self.assertEquals([entity.integer for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          integer__gte=2).order_by('integer')],
                          [2, 5, 9])

        # test filter on primary_key field
        self.assertEquals([entity.email for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          email__gte='rinnengan@sage.de').order_by('email')],
                          ['rinnengan@sage.de', 'sharingan@uchias.com', ])

    def test_lte(self):
        # test lte on float
        self.assertEquals([entity.floating_point for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          floating_point__lte=5.3).order_by('floating_point')],
                          [1.58, 2.6, 5.3])

        # test lte on integer
        self.assertEquals([entity.integer for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          integer__lte=5).order_by('integer')],
                          [1, 2, 5])

        # test filter on primary_key field
        self.assertEquals([entity.email for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          email__lte='rinnengan@sage.de').order_by('email')],
                          ['app-engine@scholardocs.com', 'rasengan@naruto.com',
                          'rinnengan@sage.de'])

    def test_equals(self):
        # test equality filter on primary_key field
        self.assertEquals([entity.email for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          email='rinnengan@sage.de').order_by('email')],
                          ['rinnengan@sage.de'])

    def test_is_null(self):
        pass

    def test_exclude(self):
        self.assertEquals([entity.email for entity in \
                            FieldsWithOptionsModel.objects.all().exclude(
                            floating_point__lt=9.1).order_by('floating_point')],
                            ['rasengan@naruto.com', 'sharingan@uchias.com',
                            'app-engine@scholardocs.com', ])

    def test_multi_filter(self):
        # additionally tests count :)
        self.assertEquals(FieldsWithOptionsModel.objects.filter(
                          floating_point__lt=5.3).filter(floating_point__gt=2.6).
                          count(), 0)
        
        # test across multiple columns. On app engine only one filter is allowed
        # to be an inequality filter
        self.assertEquals([(entity.floating_point, entity.integer) for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          floating_point__lte=5.3).filter(integer=2).order_by(
                          'floating_point')], [(2.6, 2), ])
        
        # test multiple filters including the primary_key field
        self.assertEquals([entity.email for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          email__gte='rinnengan@sage.de').filter(integer=2).order_by(
                          'email')], ['sharingan@uchias.com', ])

        # test in filter on primary key with another arbitrary filter
        self.assertEquals([entity.email for entity in \
                          FieldsWithOptionsModel.objects.filter(
                          email__in=['rinnengan@sage.de',
                          'sharingan@uchias.com']).filter(integer__gt=2).order_by(
                          'integer')], ['rinnengan@sage.de', ])

        # Test exceptions

        # test multiple filters exception when filtered and not ordered against
        # the first filter
        self.assertRaises(BadArgumentError, FieldsWithOptionsModel.objects.filter(
                email__gte='rinnengan@sage.de').filter(floating_point=5.3).order_by(
                'floating_point').get)

        # test exception if filtered across multiple columns with inequality filter
        self.assertRaises(BadFilterError, FieldsWithOptionsModel.objects.filter(
                          floating_point__lte=5.3).filter(integer__gte=2).order_by(
                          'floating_point').get)

        # test exception if filtered across multiple columns with inequality filter
        # with exclude
        self.assertRaises(BadFilterError, FieldsWithOptionsModel.objects.filter(
                            email__lte='rinnengan@sage.de').exclude(
                            floating_point__lt=9.1).order_by('email').get)

        self.assertRaises(BadArgumentError, FieldsWithOptionsModel.objects.all().exclude(
                            floating_point__lt=9.1).order_by('email').get)

        # TODO: Add slice tests
        # TODO: Add tests with Q objects
        # TODO: Write isnull test
        # TODO: Check all possible exceptions


    def test_pk_in(self):
        # pk_in is tested in order.py
        pass