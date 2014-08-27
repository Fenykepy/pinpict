from django.contrib import admin

from board.models import Board, Pin, Resource

admin.site.register(Board)
admin.site.register(Pin)
admin.site.register(Resource)
