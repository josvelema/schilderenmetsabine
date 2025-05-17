# workshop model
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from base.blocks import HomeStreamBlock, WorkshopSessionBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail import blocks
from django.utils.timezone import now
from wagtail.images.blocks import ImageChooserBlock


class WorkshopIndexPage(Page):
    intro = RichTextField(blank=True)

    subpage_types = ['workshops.WorkshopPage']

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]
    
    parent_page_types = ['home.HomePage', 'wagtailcore.Page']


    def get_context(self, request):
        context = super().get_context(request)
        context['workshops'] = self.get_children().live().order_by('first_published_at')
        return context


class WorkshopPage(Page):
    sessions = StreamField(
    blocks.StreamBlock([
        ("session", WorkshopSessionBlock()),
    ]),
    blank=True,
    use_json_field=True,
    verbose_name="Sessies",
    help_text="Voeg hier de data en tijden van de workshop toe."
    )
    location = models.CharField(max_length=255)
    
    workshop_image = models.ForeignKey(
    'wagtailimages.Image',
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='+',
    help_text='Afbeelding voor de workshop kaart',
    )
    
    description = StreamField(HomeStreamBlock(), use_json_field=True, blank=True)

    calendly_embed = models.URLField(
        blank=True,
        help_text="Public Calendly embed link of booking page URL (voor iframe)",
    )
    
    status_override = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optioneel: handmatig label voor teasers, bijvoorbeeld 'Nieuw!' of 'Laatste kans'."
    )
    
    STATUS_CHOICES = [
        ("open", "Nog plaatsen beschikbaar"),
        ("full", "Volgeboekt"),
        ("cancelled", "Geannuleerd"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
        verbose_name="Status van inschrijving",
        help_text="Geeft aan of deze workshop nog beschikbaar is."
    )

    parent_page_types = ['workshops.WorkshopIndexPage']
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("sessions"),
            FieldPanel("location"),
            FieldPanel("status"),
            FieldPanel("status_override"),
            FieldPanel("workshop_image"),
            FieldPanel("description"),
            FieldPanel("calendly_embed"),
        ], heading="Workshop details"),
    ]
    
    def is_past(self):
        # Bepaal of de laatste sessie in het verleden ligt
        latest_date = None
        for sessie in self.sessions:
            sessie_date = sessie.value.get('date')
            if latest_date is None or sessie_date > latest_date:
                latest_date = sessie_date
        return latest_date and latest_date < now().date()

    def get_display_status(self):
        if self.is_past():
            return "❌ Afgelopen"
        elif self.status == "open":
            return "✅ Nog plaatsen beschikbaar"
        elif self.status == "full":
            return " ❌ Volgeboekt"
        elif self.status == "cancelled":
            return "🚫 Geannuleerd"
        return ""
