from django.core.management import BaseCommand
from django.contrib.auth.models import User

from faker import Faker
from core.models import Blog

import random


class Command(BaseCommand):
    help = 'Generate fake data for the blog app'

    def add_arguments(self, parser):
        parser.add_argument('--count', help='number of records to generate')

    def handle(self, *args, **options):
        faker = Faker()
        count = int(options.get('count', 100))
        for i in range(count):
            title = faker.sentence()
            content = ' '.join(faker.paragraphs(5))
            author = random.choice(User.objects.all())
            print(f'creating blog post for {author}, title: {title}')
            Blog.objects.create(title=title, content=content, author=author)
