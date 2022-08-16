from django.urls import path
from . import views
from .views import ViewImage, PostImage, ViewBlog, ViewHeader, PutHeader, ViewMenu, ViewMenuServiceById, ViewMenuSection, ViewMenuSectionLink, PostMenuSectionLink, PostMenuSection, PostMenuService, ViewWhyUs, ViewWhyUsBlockById, PostWhyUsBlock, ViewCase, ViewCaseBlockById, PostCaseBlock, ViewCompany, ViewCompanyBlockById, PostCompanyBlock, ViewClients, ViewClientBlockById, PostClientBlock, ViewFAQ, ViewFAQBlockById, PostFAQBlock, ViewIndustry, ViewIndustryTypeById, ViewIndustryTypeBlockById, PostIndustryType, PostIndustryTypeBlock, ViewBlogBlockById, PostBlogBlock, ViewService, PostServiceType, ViewServiceTypeById, ViewServiceTypeBlockById, PostServiceTypeBlock, ViewTitle, ViewLinks

urlpatterns = [
    path('', views.index, name='index'),
    path('view/images/', ViewImage.as_view()),
    path('delete/images/', ViewImage.as_view()),
    path('post/images/', PostImage.as_view()),
    path('view/menu/', ViewMenu.as_view()),
    path('view/menu/service/', ViewMenuServiceById.as_view()),
    path('put/menu/service/', ViewMenuServiceById.as_view()),
    path('delete/menu/service/', ViewMenuServiceById.as_view()),
    path('post/menu/service/', PostMenuService.as_view()),
    path('view/menu/service/section/', ViewMenuSection.as_view()),
    path('put/menu/service/section/', ViewMenuSection.as_view()),
    path('delete/menu/service/section/', ViewMenuSection.as_view()),
    path('post/menu/service/section/', PostMenuSection.as_view()),
    path('view/menu/service/section/link/', ViewMenuSectionLink.as_view()),
    path('put/menu/service/section/link/', ViewMenuSectionLink.as_view()),
    path('post/menu/service/section/link/', PostMenuSectionLink.as_view()),
    path('delete/menu/service/section/link/', ViewMenuSectionLink.as_view()),
    path('view/header/', ViewHeader.as_view()),
    path('put/header/', PutHeader.as_view()),
    path('view/whyus/', ViewWhyUs.as_view()),
    path('put/whyus/', ViewWhyUs.as_view()),
    path('view/whyus/block/', ViewWhyUsBlockById.as_view()),
    path('put/whyus/block/', ViewWhyUsBlockById.as_view()),
    path('delete/whyus/block/', ViewWhyUsBlockById.as_view()),
    path('post/whyus/', PostWhyUsBlock.as_view()),
    path('view/case/', ViewCase.as_view()),
    path('view/case/block/', ViewCaseBlockById.as_view()),
    path('put/case/block/', ViewCaseBlockById.as_view()),
    path('delete/case/block/', ViewCaseBlockById.as_view()),
    path('post/case/block/', PostCaseBlock.as_view()),
    path('view/company/', ViewCompany.as_view()),
    path('view/company/block/', ViewCompanyBlockById.as_view()),
    path('put/company/block/', ViewCompanyBlockById.as_view()),
    path('delete/company/block/', ViewCompanyBlockById.as_view()),
    path('post/company/block/', PostCompanyBlock.as_view()),
    path('view/client/', ViewClients.as_view()),
    path('view/client/block/', ViewClientBlockById.as_view()),
    path('put/client/block/', ViewClientBlockById.as_view()),
    path('delete/client/block/', ViewClientBlockById.as_view()),
    path('post/client/block/', PostClientBlock.as_view()),
    path('view/faq/', ViewFAQ.as_view()),
    path('view/faq/block/', ViewFAQBlockById.as_view()),
    path('put/faq/block/', ViewFAQBlockById.as_view()),
    path('delete/faq/block/', ViewFAQBlockById.as_view()),
    path('post/faq/block/', PostFAQBlock.as_view()),
    path('view/industry/', ViewIndustry.as_view()),
    path('view/industry/type/', ViewIndustryTypeById.as_view()),
    path('put/industry/type/', ViewIndustryTypeById.as_view()),
    path('delete/industry/type/', ViewIndustryTypeById.as_view()),
    path('post/industry/type/', PostIndustryType.as_view()),
    path('view/industry/type/block/', ViewIndustryTypeBlockById.as_view()),
    path('put/industry/type/block/', ViewIndustryTypeBlockById.as_view()),
    path('delete/industry/type/block/', ViewIndustryTypeBlockById.as_view()),
    path('post/industry/type/block/', PostIndustryTypeBlock.as_view()),
    path('view/blog/', ViewBlog.as_view()),
    path('view/blog/block/', ViewBlogBlockById.as_view()),
    path('put/blog/block/', ViewBlogBlockById.as_view()),
    path('delete/blog/block/', ViewBlogBlockById.as_view()),
    path('post/blog/block/', PostBlogBlock.as_view()),
    path('view/service/', ViewService.as_view()),
    path('view/service/type/', ViewServiceTypeById.as_view()),
    path('put/service/type/', ViewServiceTypeById.as_view()),
    path('delete/service/type/', ViewServiceTypeById.as_view()),
    path('post/service/type/', PostServiceType.as_view()),
    path('view/service/type/block/', ViewServiceTypeBlockById.as_view()),
    path('put/service/type/block/', ViewServiceTypeBlockById.as_view()),
    path('delete/service/type/block/', ViewServiceTypeBlockById.as_view()),
    path('post/service/type/block/', PostServiceTypeBlock.as_view()),
    path('view/links/', ViewLinks.as_view()),
    path('put/links/', ViewLinks.as_view()),
    path('view/title/', ViewTitle.as_view()),
    path('put/title/', ViewTitle.as_view()),
]