from import_export import resources

from .models import Food


class FoodResource(resources.ModelResource):

    class Meta:
        model = Food
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('name', )