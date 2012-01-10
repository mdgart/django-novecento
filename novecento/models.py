from django.db import models
from novecento.conf import settings 
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _ 
from fields import OrderField 

from datetime import datetime 

if settings.USE_DJANGO_MULTILINGUAL:
	try:
		from multilingual.translation import TranslationModel
	except:
		settings.USE_DJANGO_MULTILINGUAL = False

if settings.USE_FILEBROWSER:
	try:
		from filebrowser.fields import FileBrowseField	 
	except:
		settings.USE_FILEBROWSER = False

class NovecentoSection(models.Model):
	
	if settings.USE_DJANGO_MULTILINGUAL:
		class Translation(TranslationModel):
			section = models.CharField(max_length=250, verbose_name=_("Articles section"))
			slug = models.SlugField(help_text=_('A "Slug" is a unique URL-friendly title for an object.'))
	else:
		section = models.CharField(max_length=250, verbose_name=_("Articles section"))		
		slug = models.SlugField(help_text=_('A "Slug" is a unique URL-friendly title for an object.'))
	
	class Meta:
		verbose_name = _("Articles section")
		verbose_name_plural = _("Articles sections")

	def __unicode__(self):
		return self.section if self.section else "-"

	def get_absolute_url(self):
		return reverse('novecento-section', args=[self.slug if self.slug else ""])

class NovecentoImage(models.Model):
	if settings.USE_FILEBROWSER: 
		picture = FileBrowseField(_("Image"), max_length=255, directory="uploads/images/%Y/%m/%d")
	else:
		picture = models.ImageField(upload_to="uploads/images/%Y/%m/%d", verbose_name=_("Image"))

	if settings.USE_DJANGO_MULTILINGUAL:
		class Translation(TranslationModel):
			caption = models.CharField(blank=True, null=True, max_length=250, verbose_name=_("Caption"))
	else:
		caption = models.CharField(blank=True, null=True, max_length=250, verbose_name=_("Caption"))
				
	orderby = OrderField(verbose_name=_("Order by"), help_text=_("Please, insert progressive numbers."))
	article = models.ForeignKey("NovecentoArticle", verbose_name=_("Article"))

	def thumb(self):
		if settings.USE_FILEBROWSER and self.picture:
			return '<img src="%s" />' % self.picture.url_thumbnail
		else:
			return "-"
	
	thumb.allow_tags = True

	class Meta:
		verbose_name = _("Image")
		verbose_name_plural = _("Images")
		ordering = ['orderby']
		get_latest_by = 'orderby'
		
	def __unicode__(self):
		if settings.USE_FILEBROWSER:
			return self.picture.filename
		else:
			return self.picture.url		

class NovecentoDocument(models.Model):
	
	if settings.USE_DJANGO_MULTILINGUAL:
		class Translation(TranslationModel):
			if settings.USE_FILEBROWSER: 
				document = FileBrowseField(_("Document"), max_length=255, directory="uploads/documents/%Y/%m/%d")
			else:
				document = models.FileField(upload_to="uploads/documents/%Y/%m/%d", verbose_name=_("Document"))
			description = models.TextField(blank=True, null=True, verbose_name=_("Description"))  
	else:
		if settings.USE_FILEBROWSER: 
			document = FileBrowseField(_("Document"), max_length=255, directory="uploads/documents/%Y/%m/%d")
		else:
			document = models.FileField(upload_to="uploads/documents/%Y/%m/%d", verbose_name=_("Document"))
		description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
				
	orderby = OrderField(verbose_name=_("Order by"), help_text=_("Please, insert progressive numbers."))

	class Meta:
		verbose_name = _("Document")
		verbose_name_plural = _("Documents")
		ordering = ['orderby']
		get_latest_by = 'orderby'
		
	def __unicode__(self):
		if settings.USE_FILEBROWSER:
			return self.document.filename
		else:
			return self.document.url
		
class NovecentoArticle(models.Model):

	if settings.USE_DJANGO_MULTILINGUAL:
		class Translation(TranslationModel):
			headline = models.CharField(max_length=250, verbose_name=_("Headline")) 
			slug = models.SlugField(help_text=_('A "Slug" is a unique URL-friendly title for an object.'))			
			summary = models.TextField(blank=True, null=True, verbose_name=_("Summary"), help_text=_("A single paragraph summary or preview of the article."))
			body = models.TextField(blank=True, null=True, verbose_name=_("Body text"))
			
	else:
		headline = models.CharField(max_length=250, verbose_name=_("Headline")) 
		slug = models.SlugField(help_text=_('A "Slug" is a unique URL-friendly title for an object.')) 
		summary = models.TextField(blank=True, null=True, verbose_name=_("Summary"), help_text=_("A single paragraph summary or preview of the article."))
		body = models.TextField(blank=True, null=True, verbose_name=_("Body text"))		
	
	author = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Author"))
	publish = models.BooleanField(_("Publish on site"), default=True, help_text=_('Articles will not appear on the site until their "publish date".'))
	pub_date = models.DateTimeField(default=datetime.now, verbose_name=_("Publish date")) 
	documents = models.ManyToManyField(NovecentoDocument, related_name='articles', null=True, blank=True, verbose_name=_("Documents"))
	sections = models.ManyToManyField(NovecentoSection, related_name='articles', null=True, blank=True, verbose_name=_("Sections"))
	enable_comments = models.BooleanField(default=True)			
	
	class Meta:
		verbose_name = _("Article")
		verbose_name_plural = _("Articles")
		ordering = ['-pub_date']
		get_latest_by = 'pub_date'

	def __unicode__(self):
		return self.headline if self.headline else "-"

	def get_absolute_url(self):
		args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug if self.slug else ""]
		return reverse('novecento-article-detail', args=args)	