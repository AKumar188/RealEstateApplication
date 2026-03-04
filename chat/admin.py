from django.contrib import admin
from .models import Conversation, Message


# ==========================
# Message Inline (Shows messages inside conversation)
# ==========================
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ("sender", "message_type", "content", "media_url", "is_read", "created_at")
    can_delete = False


# ==========================
# Conversation Admin
# ==========================
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "buyer", "owner", "created_at")
    search_fields = ("buyer__email", "owner__email")
    list_filter = ("created_at",)
    readonly_fields = ("id", "created_at")
    inlines = [MessageInline]


# ==========================
# Message Admin
# ==========================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "message_type", "is_read", "created_at")
    search_fields = ("sender__email", "content")
    list_filter = ("message_type", "is_read", "created_at")
    readonly_fields = ("id", "created_at")