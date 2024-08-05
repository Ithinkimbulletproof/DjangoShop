from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product


class Command(BaseCommand):
    help = 'Create moderator group and assign permissions'

    def handle(self, *args, **kwargs):
        moderator_group, created = Group.objects.get_or_create(
            name='Модератор')

        if created:
            self.stdout.write(
                self.style.SUCCESS('Group "Модератор" created'))
        else:
            self.stdout.write('Group "Модератор" already exists')

        permissions = Permission.objects.filter(
            content_type__app_label='catalog',
            codename__in=[
                'can_unpublish_product',
                'can_change_product_description',
                'can_change_product_category'
            ]
        )

        for perm in permissions:
            moderator_group.permissions.add(perm)
            self.stdout.write(
                f'Permission {perm.codename} added to group "Модератор"')

        self.stdout.write(self.style.SUCCESS(
            'Permissions assigned to group "Модератор"'))