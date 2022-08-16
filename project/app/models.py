from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
# Create your models here.


class Images(models.Model):
    image = CloudinaryField('image', null=True)


class Header(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Menu(models.Model):
    name = models.CharField(default="Menu", max_length=255)
    type = models.CharField(max_length=7, default="")
    value = models.CharField(max_length=255, default="")
    parentid = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class MenuServices(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=7, default="")
    value = models.CharField(max_length=255, default="")
    parentId = models.IntegerField(null=True)
    menu = models.ForeignKey(Menu, default=1, on_delete=models.SET_NULL, null=True, related_name="service")

    def __str__(self):
        return self.name


class MenuServicesSections(models.Model):
    name = models.CharField(max_length=255)
    parentid = models.IntegerField(null=True)
    type = models.CharField(max_length=7, default="")
    value = models.CharField(max_length=255, default="")
    menu_services = models.ForeignKey(MenuServices, default=1, on_delete=models.SET_NULL, null=True, related_name="section")

    def __str__(self):
        return self.name


class MenuSectionLinks(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=7, default="")
    value = models.CharField(max_length=255, default="")
    parentid = models.IntegerField(null=True)
    menu_section = models.ForeignKey(MenuServicesSections, on_delete=models.SET_NULL, blank=True, null=True, related_name="link")

    def __str__(self):
        return self.name


class WhyUs(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class WhyUsBlock(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    why_us = models.ForeignKey(WhyUs, on_delete=models.SET_NULL, null=True, related_name="block", default="2")

    def __str__(self):
        return self.title


class Cases(models.Model):
    name = models.CharField(default="Cases", max_length=255)

    def __str__(self):
        return self.name


class CaseBlock(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = CloudinaryField('image', null=True)
    content = models.CharField(max_length=255, null=True)
    case = models.ForeignKey(Cases, on_delete=models.SET_NULL, null=True, related_name="block", default="1")

    def __str__(self):
        return self.title


class Industries(models.Model):
    name = models.CharField(default="Industries", max_length=255)

    def __str__(self):
        return self.name


class IndustryType(models.Model):
    name = models.CharField(max_length=255)
    industry = models.ForeignKey(Industries, on_delete=models.SET_NULL, null=True, related_name="type", default="1")

    def __str__(self):
        return self.name


class IndustriesBlock(models.Model):
    title = models.CharField(max_length=255)
    image = CloudinaryField('image', null=True)
    content = models.CharField(max_length=255, null=True)
    industry_type = models.ForeignKey(IndustryType, on_delete=models.SET_NULL, null=True, related_name="block")

    def __str__(self):
        return self.title


class Companies(models.Model):
    name = models.CharField(default="Companies", max_length=255)

    def __str__(self):
        return self.name


class CompaniesBlock(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
    image = CloudinaryField('image', null=True)
    company = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True, related_name="block", default="1")

    def __str__(self):
        return self.title


class Clients(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ClientBlock(models.Model):
    full_name = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = CloudinaryField('image', null=True)
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, null=True, related_name="block", default="1")

    def __str__(self):
        return self.title


class FAQ(models.Model):
    name = models.CharField(default="FAQ", max_length=255)

    def __str__(self):
        return self.name


class FAQBlock(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    faq = models.ForeignKey(FAQ, on_delete=models.SET_NULL, null=True, related_name="block", default="1")

    def __str__(self):
        return self.title


class Blog(models.Model):
    name = models.CharField(default="Blog", max_length=255)

    def __str__(self):
        return self.name


class BlogBlock(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = CloudinaryField('image', null=True)
    content = models.CharField(max_length=255, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, related_name="block", default="1")

    def __str__(self):
        return self.title


class Services(models.Model):
    name = models.CharField(default="Services", max_length=255)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    title = models.CharField(max_length=255)
    service = models.ForeignKey(Services, on_delete=models.SET_NULL, null=True, related_name="type", default="1")

    def __str__(self):
        return self.title


class ServiceTypeBlock(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = CloudinaryField('image', null=True)
    url = models.CharField(max_length=255, null=True)
    content = models.CharField(max_length=255, null=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, related_name="block")

    def __str__(self):
        return self.title


class Links(models.Model):
    mail = models.EmailField(max_length=255)
    facebook = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)

    def __str__(self):
        return "Links"


class Title(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return "Title"
