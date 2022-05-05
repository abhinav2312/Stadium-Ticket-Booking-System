from django.contrib import admin
# Register your models here.
from .models import snacks, stadium, ticket, book, matches, seats

admin.site.register(ticket)
admin.site.register(seats)
admin.site.register(matches)
admin.site.register(stadium)
admin.site.register(snacks)
admin.site.register(book)