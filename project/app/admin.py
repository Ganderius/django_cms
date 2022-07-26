from django.contrib import admin
from .models import Header, Menu, MenuServices, MenuServicesSections, MenuSectionLinks, WhyUs, WhyUsBlock, Cases, CaseBlock, Industries, IndustryType, IndustriesBlock, Companies, CompaniesBlock, Clients, ClientBlock, FAQ, FAQBlock, Blog, BlogBlock, Services, ServiceType, ServiceTypeBlock, Links, Title
# Register your models here.


class MenuServicesList(admin.TabularInline):
    fk_name = 'menu'
    model = MenuServices


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuServicesList, ]


class MenuSectionsList(admin.TabularInline):
    fk_name = 'menu_services'
    model = MenuServicesSections


@admin.register(MenuServices)
class MenuServicesAdmin(admin.ModelAdmin):
    inlines = [MenuSectionsList, ]


class MenuLinksList(admin.TabularInline):
    fk_name = 'menu_section'
    model = MenuSectionLinks


@admin.register(MenuServicesSections)
class MenuLSectionsAdmin(admin.ModelAdmin):
    inlines = [MenuLinksList, ]


class WhyUsBlockList(admin.TabularInline):
    fk_name = 'why_us'
    model = WhyUsBlock


@admin.register(WhyUs)
class WhyUsAdmin(admin.ModelAdmin):
    inlines = [WhyUsBlockList, ]


class CasesBlockList(admin.TabularInline):
    fk_name = 'case'
    model = CaseBlock


@admin.register(Cases)
class CasesAdmin(admin.ModelAdmin):
    inlines = [CasesBlockList, ]


class IndustryTypeList(admin.TabularInline):
    fk_name = 'industry'
    model = IndustryType


@admin.register(Industries)
class IndustryAdmin(admin.ModelAdmin):
    inlines = [IndustryTypeList, ]


class IndustryBlockList(admin.TabularInline):
    fk_name = 'industry_type'
    model = IndustriesBlock


@admin.register(IndustryType)
class IndustryTypeAdmin(admin.ModelAdmin):
    inlines = [IndustryBlockList, ]


class CompanyBlockList(admin.TabularInline):
    fk_name = 'company'
    model = CompaniesBlock


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    inlines = [CompanyBlockList, ]


class ClientBlockList(admin.TabularInline):
    fk_name = 'client'
    model = ClientBlock


@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    inlines = [ClientBlockList, ]


class FAQBlockList(admin.TabularInline):
    fk_name = 'faq'
    model = FAQBlock


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    inlines = [FAQBlockList, ]


class BlogBlocksList(admin.TabularInline):
    fk_name = 'blog'
    model = BlogBlock


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogBlocksList, ]


class ServiceTypeList(admin.TabularInline):
    fk_name = 'service'
    model = ServiceType


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    inlines = [ServiceTypeList, ]


class ServiceTypeBlockList(admin.TabularInline):
    fk_name = 'service_type'
    model = ServiceTypeBlock


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    inlines = [ServiceTypeBlockList, ]


admin.site.register(Header)
admin.site.register(MenuSectionLinks)
admin.site.register(WhyUsBlock)
admin.site.register(CaseBlock)
admin.site.register(IndustriesBlock)
admin.site.register(CompaniesBlock)
admin.site.register(ClientBlock)
admin.site.register(FAQBlock)
admin.site.register(BlogBlock)
admin.site.register(ServiceTypeBlock)
admin.site.register(Links)
admin.site.register(Title)
