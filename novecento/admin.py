from django.contrib import admin
from models import NovecentoArticle, NovecentoImage, NovecentoDocument, NovecentoSection 
from novecento.conf import settings 

if settings.USE_DJANGO_MULTILINGUAL:
	try:
		from multilingual.admin import MultilingualModelAdmin
		ma = MultilingualModelAdmin
	except:
		settings.USE_DJANGO_MULTILINGUAL = False 
		ma = admin.ModelAdmin

class ImageInline(admin.TabularInline):
	model = NovecentoImage
	extra = 1
	# if grappelli is used, allow add new images from the inline form
	try:
		allow_add = True
	except:
		pass 

class NovecentoArticleAdmin(ma):
	if settings.USE_DJANGO_MULTILINGUAL:
		use_prepopulated_fields = {'slug': ('headline',)}
	else:
		prepopulated_fields = {'slug': ('headline',)}
	list_display = ('headline', 'author', 'pub_date', 'publish')
	list_filter = ['pub_date']
	date_hierarchy = 'pub_date'
	save_as = True
	inlines = [ ImageInline, ] 
	
	
class NovecentoImageAdmin(admin.ModelAdmin):
	list_display = ('picture', 'caption', 'thumb')
	search_fields = ['caption'] 

class NovecentoDocumentAdmin(admin.ModelAdmin):
	list_display = ('document', 'description')
	search_fields = ['description'] 

class NovecentoSectionAdmin(ma):
	if settings.USE_DJANGO_MULTILINGUAL:
			use_prepopulated_fields = {'slug': ('section',)}
	else:
		prepopulated_fields = {'slug': ('section',)} 
	list_display = ('section',)

admin.site.register(NovecentoArticle, NovecentoArticleAdmin)
admin.site.register(NovecentoDocument, NovecentoDocumentAdmin)
admin.site.register(NovecentoImage, NovecentoImageAdmin) 
admin.site.register(NovecentoSection, NovecentoSectionAdmin)
												