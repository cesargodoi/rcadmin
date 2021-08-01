import random
import factory

from faker import Faker
from django.utils import timezone
from user.models import User, Profile
from center.models import Center
from publicwork.models import TempRegOfSeeker, Seeker

fake = Faker("pt_BR")
get_gender = random.choice(["M", "F"])


#  User
class UserFactory(factory.django.DjangoModelFactory):
    Faker.seed()

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

    name = f"Center {fake.pyint(min_value=1, max_value=9)}"
    short_name = f"C-{name.split()[1]}"
    city = fake.city()
    state = fake.estado_sigla()
    country = fake.current_country_code()
    phone_1 = fake.phone_number()
    email = fake.email()
    center_type = "CNT"


#  TempRegOfSeeker
class TempRegOfSeeker(factory.django.DjangoModelFactory):
    class Meta:
        model = TempRegOfSeeker

    name = fake.name()
    birth = fake.date_of_birth(maximum_age=80)
    gender = get_gender
    city = fake.city()
    state = fake.estado_sigla()
    country = "BR"
    solicited_on = timezone.now()


#  Seeker
class SeekerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Seeker

    name = fake.name()
    birth = fake.date_of_birth(maximum_age=80)
    gender = random.choice(["M", "F"])
    city = fake.city()
    state = fake.estado_sigla()
    country = "BR"
    solicited_on = timezone.now()
