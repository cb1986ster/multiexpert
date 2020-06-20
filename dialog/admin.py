from django.contrib import admin
from .models import Statement, Anwser, Page

# Register your models here.
admin.site.register(Statement)
admin.site.register(Page)


def set_accepted(model_admin, request, query_set):
    query_set.update(accepted=True)

set_accepted.short_description = "Ustaw jako zaakceptowany"

def set_not_accepted(model_admin, request, query_set):
    query_set.update(accepted=False)

set_not_accepted.short_description = "Ustaw jako NIE zaakceptowany"

@admin.register(Anwser)
class AnwserAdmin(admin.ModelAdmin):
    actions = (set_accepted, set_not_accepted)
    list_display = ( "text", "accepted" )
