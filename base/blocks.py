# base/blocks.py
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import DateBlock, TimeBlock, StructBlock, ListBlock, CharBlock, RichTextBlock, URLBlock, PageChooserBlock, BooleanBlock
from wagtail.embeds.blocks import EmbedBlock
from django.core.exceptions import ValidationError



class CaptionedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = "image"
        template = "base/blocks/captioned_image_block.html"

      

class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=False)
    image = ImageChooserBlock(required=False)
    link_text = blocks.CharBlock(required=False, default="Lees meer")
    link_page = PageChooserBlock(required=False)
    link_url = blocks.URLBlock(required=False)

    class Meta:
        icon = "doc-full"
        template = "base/blocks/card_block.html"

    def get_url(self):
        if self.link_page:
            return self.link_page.url
        return self.link_url

    def clean(self, value):
        errors = {}
        link_page = value.get('link_page')
        link_url = value.get('link_url')

        if link_page and link_url:
            errors['link_url'] = ValidationError("Gebruik óf een interne pagina óf een externe URL, niet allebei.")
            errors['link_page'] = ValidationError("Gebruik óf een interne pagina óf een externe URL, niet allebei.")

        if not link_page and not link_url:
            errors['link_url'] = ValidationError("Geef minstens een link op (pagina of URL).")

        if errors:
            raise ValidationError('Ongeldige linkconfiguratie', params=errors)

        return super().clean(value)



class CardGridBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    cards = blocks.ListBlock(CardBlock())

    class Meta:
        icon = "placeholder"
        template = "base/blocks/card_grid_block.html"


class SectionBlock(blocks.StructBlock):
    heading = blocks.CharBlock(required=False)
    content = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
        ('image', CaptionedImageBlock()),
        ('embed', EmbedBlock()),
        ('card', CardBlock()),
        ('card_grid', CardGridBlock()),
    ])

    class Meta:
        icon = "placeholder"
        template = "base/blocks/section_block.html"
        
class ImageScrollerBlock(StructBlock):
    images = ListBlock(
        ImageChooserBlock(),
        label="Afbeeldingen",
        help_text="Voeg een of meerdere afbeeldingen toe"
    )
    show_controls = BooleanBlock(
        required=False,
        default=True,
        label="Toon navigatieknoppen",
        help_text="Schakel aan/uit of gebruikers zelf door afbeeldingen kunnen klikken"
    )

    class Meta:
        icon = "image"
        label = "Image Scroller"
        template = "base/blocks/image_scroller_block.html"


class WorkshopTeaserBlock(StructBlock):
    workshop_page = PageChooserBlock(target_model='workshops.WorkshopPage')
    custom_label = CharBlock(required=False, help_text="Optioneel: label zoals 'Nieuw', 'Laatste kans', etc.")
    override_image = ImageChooserBlock(required=False, help_text="Optioneel: afbeelding overschrijven")

    class Meta:
        icon = "pick"
        template = "base/blocks/workshop_teaser_block.html"
        

class CalendlyEmbedBlock(blocks.StructBlock):
    url = blocks.URLBlock(help_text="Plak hier je Calendly link, bijvoorbeeld: https://calendly.com/schilderenmetsabine-info/30min")

    class Meta:
        icon = "form"
        label = "Calendly Embed"
        template = "base/blocks/calendly_embed_block.html"


class WorkshopSessionBlock(StructBlock):
    date = DateBlock(required=True, help_text="Datum van de workshop")
    start_time = TimeBlock(required=True, help_text="Starttijd")
    end_time = TimeBlock(required=True, help_text="Eindtijd")

    class Meta:
        icon = "date"
        label = "Workshop Sessie"
        
        
from wagtail.blocks import StructBlock, CharBlock, BooleanBlock, TextBlock, EmailBlock, ChoiceBlock

class TextInputBlock(StructBlock):
    label = CharBlock()
    required = BooleanBlock(required=False, default=True)
    help_text = CharBlock(required=False)

    class Meta:
        icon = "user"
        label = "Tekstveld"

class EmailInputBlock(StructBlock):
    label = CharBlock()
    required = BooleanBlock(required=False, default=True)
    help_text = CharBlock(required=False)

    class Meta:
        icon = "mail"
        label = "E-mailveld"

class TextAreaBlock(StructBlock):
    label = CharBlock()
    required = BooleanBlock(required=False, default=True)
    help_text = CharBlock(required=False)

    class Meta:
        icon = "form"
        label = "Tekstvak (groot)"

class CheckboxBlock(StructBlock):
    label = CharBlock()
    help_text = CharBlock(required=False)

    class Meta:
        icon = "tick"
        label = "Checkbox"


class HomeStreamBlock(blocks.StreamBlock):
    section = SectionBlock()
    paragraph = blocks.RichTextBlock()
    image = CaptionedImageBlock()
    embed = EmbedBlock()
    card_grid = CardGridBlock()
    card = CardBlock()
    calendly = CalendlyEmbedBlock()
    workshop_teaser = WorkshopTeaserBlock()
    image_scroller = ImageScrollerBlock()
   