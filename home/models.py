from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from base.blocks import HomeStreamBlock
from wagtail.fields import StreamField

class HomePage(Page):
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text='afbeelding voor de hero sectie',
    )
    hero_title = models.CharField(blank=True, max_length=255, help_text='titel van website')
    hero_text = models.CharField(blank=True, max_length=255, help_text='subtitel van website')
    hero_cta = models.CharField(blank=True, max_length=255, help_text='call to action tekst')
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text='link naar pagina waar de call to action naartoe gaat',
    )
    body = StreamField(HomeStreamBlock(), blank=True, use_json_field=True)

    parent_page_types = ['wagtailcore.Page']
    

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_image"),
            FieldPanel("hero_title"),
            FieldPanel("hero_text"),
            FieldPanel("hero_cta"),
            FieldPanel("hero_cta_link"),
        ], heading="Hero"),
        FieldPanel("body"),
    ]
