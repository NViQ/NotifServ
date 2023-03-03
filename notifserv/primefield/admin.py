from django.contrib import admin
from .models import Mailing, Clients #Teg, Code_operators
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'teg', 'code_operator')
    list_display_links = ('id', 'phone')

class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_mailing', 'finish_mailing')
    list_display_links = ('id', 'start_mailing')

# class TegAdmin(admin.ModelAdmin):
#     list_display = ('teg',)
#     list_display_links = ('teg',)
#
# class Code_operatorsAdmin(admin.ModelAdmin):
#     list_display = ('code_operator',)
#     list_display_links = ('code_operator',)


admin.site.register(Mailing, MailingAdmin)
admin.site.register(Clients, ClientsAdmin)
# admin.site.register(Teg, TegAdmin)
# admin.site.register(Code_operators, Code_operatorsAdmin)
