from django.contrib import admin
from question.models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text', 'owner']}),
        ('Date information', {'fields': ['creation_date', 'start_date', 'end_date'], 'classes': ['collapse']}),
    ]

    inlines = [ChoiceInline]

    ordering = ['-id']
    list_per_page = 200
    list_display = ('text', 'creation_date', 'start_date', 'end_date', 'owner')


admin.site.register(Question, QuestionAdmin)
