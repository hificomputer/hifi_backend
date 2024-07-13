from typing import Any
from .cat_utils import load_cat_tree, check_cat_tree, check_cat_groups, CategoryConfigNotFoundError
from django.core.management import BaseCommand
from hificom.models import Category
from .categories import cat_tree, cat_groups


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        try:
            check_cat_tree(cat_tree)
        except CategoryConfigNotFoundError as e:
            self.stdout.write("Tree check failded. Details: {}".format(str(e)), self.style.ERROR)
        except Exception as e:
            self.stdout.write("Tree check failded. Details: {}".format(str(e)), self.style.ERROR)
            return
        try:
            check_cat_groups(cat_groups)
        except CategoryConfigNotFoundError as e:
            self.stdout.write("Category group checking failded. Details: {}".format(str(e)), self.style.ERROR)
        except Exception as e:
            self.stdout.write("Category group checking failded. Details: {}".format(str(e)), self.style.ERROR)
            return
        load_cat_tree(cat_tree)
        self.stdout.write("Categories loaded", self.style.SUCCESS)

