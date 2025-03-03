# Register your models here.
from django.contrib import admin
from .models import Task  # Import your model

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'completed', 'created_at')  # Customize displayed fields
    search_fields = ('title',)  # Enable search by title
    list_filter = ('completed',)  # Enable filtering
