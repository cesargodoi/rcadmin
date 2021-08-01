from user.tests.dummy import UserDummy
from center.models import Center


class CenterDummy(UserDummy):
    @classmethod
    def setUpTestData(cls):
        super(CenterDummy, cls).setUpTestData()
        
        # centers
        cls.center_1 = Center.objects.create(
            name="Aquarius",
            short_name="Aquarius",
            phone_1="(11)8765-4321",
            phone_2="11987654321",
            address="R. Sebastião Carneiro",
            number="215",
            city="São Paulo",
            state="sp",
            country="Brasil",
            zip_code="01543-020",
            secretary=cls.office1,
        )
        cls.center_2 = Center.objects.create(
            name="Campinas",
            short_name="Campinas",
            phone_1="(11)8765-4321",
            phone_2="11987654321",
            address="R. Campineiros Selvagens",
            number="200",
            city="Campinas",
            state="sp",
            country="Brasil",
            zip_code="01543-020",
            secretary=cls.office2,
        )
