from django.contrib import admin
from models import *

#class CircleAdmin(admin.ModelAdmin):
    #list_display = ('title', 'teacher')
    #filter_horizontal = ('users',)

#class GenreAdmin(admin.ModelAdmin):
    #list_display = ('name', 'image')

#class SongAdmin(admin.ModelAdmin):
    #list_display = ('time', 'user', 'title', 'description', 'circle', 'genre')

#admin.site.register(Circle, CircleAdmin)
#admin.site.register(Genre, GenreAdmin)
#admin.site.register(Song, SongAdmin)
#admin.site.register(Comment)

admin.site.register(Circle)
admin.site.register(Genre)
admin.site.register(Song)
admin.site.register(Comment)
admin.site.register(Inspiration)
