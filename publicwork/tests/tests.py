import pytest
from center.models import Center


@pytest.mark.django_db
def test_try_to_create_center(center_factory):
    center_factory.create()
    assert Center.objects.count() == 1
