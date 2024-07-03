from django.contrib import admin
from .models import Simple, DateExample, NullExample, Language, Framework, Movie, Character

admin.site.register(Simple)
admin.site.register(DateExample)
admin.site.register(NullExample)
admin.site.register(Language)
admin.site.register(Framework)
admin.site.register(Movie)
admin.site.register(Character)