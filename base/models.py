from wagtail.contrib.forms.models import AbstractEmailForm
from wagtail.fields import StreamField
from base.blocks import *
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django import forms
from django.template.response import TemplateResponse


class ContactFormPage(AbstractEmailForm):
    intro = StreamField(HomeStreamBlock(), blank=True, use_json_field=True)
    thank_you = StreamField(HomeStreamBlock(), blank=True, use_json_field=True)
    form_fields = StreamField([
        ("text", TextInputBlock()),
        ("email", EmailInputBlock()),
        ("textarea", TextAreaBlock()),
        ("checkbox", CheckboxBlock()),
    ], use_json_field=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        FieldPanel("form_fields"),
        FieldPanel("thank_you"),
        MultiFieldPanel([
            FieldPanel("from_address"),
            FieldPanel("to_address"),
            FieldPanel("subject"),
        ], heading="Email instellingen"),
    ]

    def get_form_class(self):
        fields = {}
        for block in self.form_fields:
            b = block.block
            v = block.value

            if block.block_type == "text":
                fields[v["label"]] = forms.CharField(
                    required=v.get("required", True),
                    help_text=v.get("help_text", ""),
                    widget=forms.TextInput(attrs={"class": "text-input"})
                )
            elif block.block_type == "email":
                fields[v["label"]] = forms.EmailField(
                    required=v.get("required", True),
                    help_text=v.get("help_text", ""),
                    widget=forms.EmailInput(attrs={"class": "email-input"})
                )
            elif block.block_type == "textarea":
                fields[v["label"]] = forms.CharField(
                    required=v.get("required", True),
                    help_text=v.get("help_text", ""),
                    widget=forms.Textarea(attrs={"class": "textarea-input"})
                )
            elif block.block_type == "checkbox":
                fields[v["label"]] = forms.BooleanField(
                    required=False,
                    help_text=v.get("help_text", ""),
                )
        return type('CustomForm', (forms.Form,), fields)

    def serve(self, request):
        form_class = self.get_form_class()

        if request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data
                send_mail(
                    subject=self.subject,
                    message="\n".join(f"{k}: {v}" for k, v in cleaned.items()),
                    from_email=self.from_address,
                    recipient_list=[self.to_address],
                )
                return TemplateResponse(request, self.get_template(request), {
                'page': self,
                'self': self,
                'form_submission_success': True,
                })
        else:
            form = form_class()

        return TemplateResponse(request, self.get_template(request), {
        'page': self,
        'self': self,  # 👈 DIT IS BELANGRIJK
        'form': form,
        })


    def get_context(self, request):
        context = super().get_context(request)
        context["form"] = self.get_form_class()()
        return context


    class Meta:
        verbose_name = "Contact Form Page"
        verbose_name_plural = "Contact Form Pages"