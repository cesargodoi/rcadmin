import random
import factory

from faker import Faker
from user.models import User, Profile
from center.models import Center
from event.models import Activity
from treasury.models import PayTypes, BankFlags

from rcadmin.common import PAY_TYPES


fake = Faker("pt_BR")
get_gender = random.choice(["M", "F"])


#  User
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = fake.email()
    is_staff = True


#  Profile
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    social_name = fake.name()
    gender = get_gender
    address = fake.street_name()
    number = fake.building_number()
    district = fake.bairro()
    city = fake.city()
    state = fake.estado_sigla
    country = fake.current_country_code()
    zip_code = fake.postcode()
    phone_1 = fake.phone_number()
    email = fake.email()


#  Center
class CenterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Center

    name = f"Center {fake.pyint(min_value=1, max_value=100)}"
    short_name = f"C-{name.split()[1]}"
    city = fake.city()
    state = fake.estado_sigla()
    country = fake.current_country_code()
    phone_1 = fake.phone_number()
    email = fake.email()
    center_type = "CNT"
    mentoring = True
    treasury = True
    publicwork = True
    accommodation = True
    made_by = factory.SubFactory(UserFactory)


#  Activity
class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    name = f"Activity {fake.pyint(min_value=1, max_value=9)}"
    activity_type = "SRV"
    multi_date = False


#  PayTypes
class PaytypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PayTypes

    name = f"PayType {fake.pyint(min_value=1, max_value=9)}"
    pay_type = random.choice([pt[0] for pt in PAY_TYPES])


#  BankFlags
class BankflagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankFlags

    name = f"BankFlag {fake.pyint(min_value=1, max_value=9)}"
    is_active = True
