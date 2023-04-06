from factory.django import DjangoModelFactory
from webapp.models import Client, Group, Coach
import factory


class CoachFactory(DjangoModelFactory):
    class Meta:
        model = Coach

    telegram_name = factory.Faker('sentence', nb_words=1)
    phone = factory.Faker('sentence', nb_words=1)
    first_name = factory.Faker('sentence', nb_words=1)
    last_name = factory.Faker('sentence', nb_words=1)
    email = factory.Faker('sentence', nb_words=1)
    started_to_work = factory.Faker('date')
    description = factory.Faker('sentence', nb_words=5)


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker('sentence', nb_words=3)
    start_at = factory.Faker('time')
    coach = factory.SubFactory(CoachFactory)


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
    phone = factory.Faker('sentence', nb_words=1)
    comment = factory.Faker('sentence', nb_words=3)
    region = factory.Faker('sentence', nb_words=1)
    group = factory.SubFactory(GroupFactory)
