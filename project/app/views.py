import uuid
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework import permissions
from cloudinary import CloudinaryImage
from .models import Images, Header, Menu, MenuServices, MenuServicesSections, MenuSectionLinks, WhyUs, WhyUsBlock, Cases, CaseBlock, Industries, IndustryType, IndustriesBlock, Companies, CompaniesBlock, Clients, ClientBlock, FAQ, FAQBlock, Blog, BlogBlock, Services, ServiceType, ServiceTypeBlock, Links, Title
import json
import urllib
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import cloudinary


def index(request):
    return HttpResponse("Hello world!")


@method_decorator(csrf_exempt, name='dispatch')
class ViewImage(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        images = Images.objects.all()

        image_data = []
        for i in images:
            image_data.append({
                'image id': i.id,
                'image name': i.image.public_id,
                'image url': i.image.url,
            })
        data = {
            'images': image_data
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        image = Images.objects.get(id=put_body.get('id'))
        image.delete()

        data = {
            'message': 'Image has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostImage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        img = request.FILES['image']
        image_data = {
            'image': img
        }

        image_new = Images.objects.create(**image_data)

        data = {
            'message': 'New image has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewHeader(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        header = Header.objects.get(id=1)
        data = {
            'id': header.id,
            'title': header.title,
            'description': header.description,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PutHeader(View):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        header = Header.objects.get(id=1)
        put_body = json.loads(request.body)
        header.title = put_body.get('title')
        header.description = put_body.get('description')

        data = {
            'message': 'Header has been changed'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewMenu(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        menu = Menu.objects.get(id=1)
        services = []
        sections = []
        links = []
        link_kost = 0
        section_kost = 0

        for i in menu.service.all():
            # print(i.name + " id: " + str(i.id))
            links.clear()
            if i.type == "link":
                services.append({
                    'id': i.id,
                    'name': i.name,
                    'parent id': i.parentId,
                    'type': i.type,
                    'value': i.value,
                })
            else:
                for j in i.section.all():
                    # print(j.name + " id: " + str(j.id))
                    if j.type == "link":
                        sections.append({
                            'id': j.id,
                            'name': j.name,
                            'parent id': j.parentid,
                            'type': j.type,
                            'value': j.value,
                        })
                        section_kost += 1
                    else:
                        for g in j.link.all():
                            # print(g.name + " id: " + str(g.id))
                            # print("parent id: " + str(g.parentid) + "\n" + "id: " + str(j.id))
                            if g.parentid == j.id:
                                links.append({
                                    'id': g.id,
                                    'name': g.name,
                                    'parent id': g.parentid,
                                    'type': g.type,
                                    'value': g.value,
                                })
                            link_kost += 1
                        link_kost *= -1
                        # print("links:")
                        # print("link_kost: " + str(link_kost))
                        # print(links[link_kost:])
                        sections.append({
                            'id': j.id,
                            'name': j.name,
                            'parent id': j.parentid,
                            'type': j.type,
                            'value': j.value,
                            'items': links[link_kost:],
                        })
                        section_kost += 1
                        # print("sections 1:")
                        # print(sections)
                        link_kost = 0
                        # links.clear()
                section_kost *= -1
                services.append({
                    'id': i.id,
                    'name': i.name,
                    'parent id': i.parentId,
                    'type': i.type,
                    'value': i.value,
                    'items': sections[section_kost:],
                })
                # print("services: ")
                # print(services)
                # sections.clear()
                section_kost = 0

        data = {
            'id': menu.id,
            'name': menu.name,
            'parent id': menu.parentid,
            'type': menu.type,
            'value': menu.value,
            'items': services,
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewMenuServiceById(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        service_id = put_body.get('id')
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=service_id)
        link_kost = 0
        section_kost = 0
        if service.type == "link":
            data = {
                'id': service.id,
                'name': service.name,
                'parent id': service.parentId,
                'type': service.type,
                'value': service.value,
            }
        else:
            section_list = []
            print(service.section)
            for i in service.section.all():
                if i.type == "link":
                    section_list.append({
                        'id': i.id,
                        'name': i.name,
                        'parent id': i.parentid,
                        'type': i.type,
                        'value': i.value,
                    })
                    section_kost += 1
                else:
                    links_list = []
                    for j in i.link.all():
                        links_list.append({
                            'id': j.id,
                            'name': j.name,
                            'parent id': j.parentid,
                            'type': j.type,
                            'value': j.value,
                        })
                        link_kost += 1
                    link_kost *= -1
                    section_list.append({
                        'id': i.id,
                        'name': i.name,
                        'parent id': i.parentid,
                        'type': i.type,
                        'value': i.value,
                        'items': links_list[link_kost:]
                    })
                    section_kost += 1
                    link_kost += 1
                section_kost *= -1
                data = {
                    'id': service.id,
                    'name': service.name,
                    'parent id': service.parentId,
                    'type': service.type,
                    'value': service.value,
                    'items': section_list[section_kost:]
                }

        return JsonResponse(data)

    def put(self, request):
        put_body = json.loads(request.body)
        service_id = put_body.get('id')
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=service_id)

        service.name = put_body.get("name")
        service.type = put_body.get("type")
        service.value = put_body.get("value")
        service.save()

        data = {
            'message': 'Service has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        service_id = put_body.get('id')
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=service_id)
        service.delete()

        data = {
            'message': 'Service has been changed'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostMenuService(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        new_service = {
            'name': put_body.get("name"),
            'parentId': 1,
            'type': put_body.get("type"),
            'value': put_body.get("value"),
        }
        service = menu.service.create(**new_service)
        for i in service.section.all():
            i.delete()

        data = {
            'message': 'New section has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewMenuSection(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        service_id = put_body.get('service id')
        section_id = put_body.get('id')
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=service_id)
        section = service.section.get(id=section_id)
        if section.type == "link":
            data = {
                'id': section.id,
                'name': section.name,
                'parent id': section.parentid,
                'type': section.type,
                'value': section.value,
            }
        else:
            links_list = []
            for i in section.link.all():
                links_list.append({
                    'id': i.id,
                    'name': i.name,
                    'parent id': i.parentid,
                    'type': i.type,
                    'value': i.value,
                })

            data = {
                'id': section.id,
                'name': section.name,
                'parent id': section.parentid,
                'type': section.type,
                'value': section.value,
                'items': links_list,
            }

        return JsonResponse(data)

    def put(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=put_body.get("service id"))
        section = service.section.get(id=put_body.get("id"))
        section.name = put_body.get("name")
        section.type = put_body.get("type")
        section.value = put_body.get("value")
        section.save()

        data = {
            'message': 'Section has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=put_body.get("service id"))
        section = service.section.get(id=put_body.get("id"))
        section.delete()

        data = {
            'message': 'Section has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostMenuSection(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=put_body.get("service id"))
        new_section = {
            'name': put_body.get("name"),
            'parentid': put_body.get("service id"),
            'type': put_body.get("type"),
            'value': put_body.get("value"),
        }

        section = service.section.create(**new_section)
        for i in section.link.all():
            i.delete()

        data = {
            'message': 'New section has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewMenuSectionLink(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=put_body.get("service id"))
        section = service.section.get(id=put_body.get("section id"))
        link = section.link.get(id=put_body.get("id"))

        data = {
            'id': link.id,
            'name': link.name,
            'parent id': link.parentid,
            'type': link.type,
            'value': link.value,
        }

        return JsonResponse(data)

    def put(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=put_body.get("service id"))
        section = service.section.get(id=put_body.get("section id"))
        link = section.link.get(id=put_body.get("id"))

        link.name = put_body.get("name")
        link.type = put_body.get("type")
        link.value = put_body.get("value")
        link.save()

        data = {
            'message': 'Link has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=put_body.get("service id"))
        section = service.section.get(id=put_body.get("section id"))
        link = section.link.get(id=put_body.get("id"))
        link.delete()

        data = {
            'message': 'Link has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostMenuSectionLink(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        menu = Menu.objects.get(id=1)
        service = menu.service.get(id=put_body.get("service id"))
        section = service.section.get(id=put_body.get("section id"))
        new_link = {
            'name': put_body.get("name"),
            'parentid': put_body.get("section id"),
            "type": put_body.get("type"),
            "value": put_body.get("value"),
        }

        link = section.link.create(**new_link)

        data = {
            'message': 'New link has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewWhyUs(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        why_us = WhyUs.objects.get(id=2)
        blocks_list = []
        for i in why_us.block.all():
            blocks_list.append({
                'id': i.id,
                'title': i.title,
                'description': i.description,
            })

        data = {
            'name': why_us.title,
            'description': why_us.description,
            'blocks': blocks_list,
        }

        return JsonResponse(data)

    def put(self, request):
        why_us = WhyUs.objects.get(id=2)
        put_body = json.loads(request.body)
        why_us.title = put_body.get('title')
        why_us.description = put_body.get('description')
        why_us.save()

        data = {
            'message': 'Why us has been changed'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewWhyUsBlockById(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = WhyUsBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'title': block.title,
            'description': block.description,
        }

        return JsonResponse(data)

    def put(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = WhyUsBlock.objects.get(id=block_id)
        block.title = put_body.get('title')
        block.description = put_body.get('description')
        block.save()

        data = {
            'message': f'Block with id: {block_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = WhyUsBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostWhyUsBlock(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        why_us = WhyUs.objects.get(id=2)
        block_data = {
            'title': put_body.get('title'),
            'description': put_body.get('description'),
        }

        block_new = why_us.block.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewCase(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        case = Cases.objects.get(id=1)
        blocks_list = []
        for i in case.block.all():
            blocks_list.append({
                'id': i.id,
                'title': i.title,
                'description': i.description,
                'previewimage': i.image.url,
                'image id': i.image.public_id,
                'content': i.content,
            })

        data = {
            'name': case.name,
            'blocks': blocks_list,
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewCaseBlockById(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = CaseBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'title': block.title,
            'description': block.description,
            'previewimage': block.image.url,
            'image id': block.image.public_id,
            'content': block.content,
        }

        return JsonResponse(data)

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        # img_extension = os.path.split(img.name)[1]
        # save_path = "media/image/"
        # if not os.path.exists(save_path):
        #     os.makedirs(os.path.dirname(save_path), exist_ok=True)
        #
        # img_save_path = "%s/%s" % (save_path, img_extension)
        # with open(img_save_path, "wb+") as f:
        #     for chunk in img.chunks():
        #         f.write(chunk)
        block = CaseBlock.objects.get(id=put_body.get('id'))
        block.image = img
        block.title = put_body.get('title')
        block.description = put_body.get('description')
        block.content = put_body.get('content')
        block.save()
        request_data = {
            'message': 'success'
        }

        return JsonResponse(request_data)

    # def put(self, request):
    #     put_body = json.loads(request.body)
    #     block_id = put_body.get('id')
    #     block = CaseBlock.objects.get(id=block_id)
    #     put_body = json.loads(request.body)
    #     block.title = put_body.get('title')
    #     block.description = put_body.get('description')
    #     block.content = put_body.get('content')
    #     #block.image = put_body.get('image id')
    #     # block.content = put_body.get('content')
    #     # image_url = put_body.get('image url')
    #     # a = []
    #     # for i in image_url:
    #     #     if i == '/':
    #     #         a.append('\\')
    #     #     else:
    #     #         a.append(i)
    #     # b = ''.join(a)
    #     # print(r'{}'.format(b))
    #     # name = urlparse(r'{}'.format(b)).path.split('/')[-1]
    #     # response = requests.get(r'{}'.format(b))
    #     # block.image.save(name, ContentFile(response.content), save=True)
    #     # print(block.image.url)
    #     block.save()
    #
    #     data = {
    #         'message': f'Block with id: {block_id} has been changed'
    #     }
    #
    #     return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = CaseBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostCaseBlock(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        block_data = {
            'title': put_body.get('title'),
            'description': put_body.get('description'),
            'image': img,
            'content': put_body.get('content')
        }

        block_new = CaseBlock.objects.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewCompany(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        company = Companies.objects.get(id=1)
        blocks_list = []
        for i in company.block.all():
            blocks_list.append({
                'id': i.id,
                'title': i.title,
                'previewimage': i.image.url,
                'image id': i.image.public_id,
                'url': i.url,
            })

        data = {
            'name': company.name,
            'blocks': blocks_list,
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewCompanyBlockById(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = CompaniesBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'title': block.title,
            'previewimage': block.image.url,
            'image id': block.image.public_id,
            'url': block.url,
        }

        return JsonResponse(data)

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        block_id = put_body.get('id')
        block = CompaniesBlock.objects.get(id=block_id)
        block.title = put_body.get('title')
        block.image = img
        block.url = put_body.get('url')
        block.save()

        data = {
            'message': f'Block with id: {block_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = CompaniesBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostCompanyBlock(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image

        block_data = {
            'title': put_body.get('title'),
            'image': img,
            'url': put_body.get('url'),
        }

        block_new = CompaniesBlock.objects.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewClients(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        client = Clients.objects.get(id=1)
        blocks_list = []
        for i in client.block.all():
            blocks_list.append({
                'id': i.id,
                'full name': i.full_name,
                'title': i.title,
                'description': i.description,
                'previewimage': i.image.url,
                'image id': i.image.public_id,
            })

        data = {
            'name': client.title,
            'blocks': blocks_list,
        }

        return JsonResponse(data)

    def put(self, request):
        client = Clients.objects.get(id=1)
        put_body = json.loads(request.body)
        client.title = put_body.get('title')
        client.description = put_body.get('description')
        client.save()

        data = {
            'message': 'Why us has been changed'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewClientBlockById(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = ClientBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'full name': block.full_name,
            'title': block.title,
            'description': block.description,
            'previewimage': block.image.url,
            'image id': block.image.public_id,
        }

        return JsonResponse(data)

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        block_id = put_body.get('id')
        block = ClientBlock.objects.get(id=block_id)
        block.full_name = put_body['full name'] #Program says its a 'dict'
        block.title = put_body.get('title')
        block.description = put_body.get('description')
        block.image = img
        block.save()

        data = {
            'message': f'Block with id: {block_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = ClientBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostClientBlock(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image

        block_data = {
            'full_name': put_body.get('full name'),
            'title': put_body.get('title'),
            'description': put_body.get('description'),
            'image': img
        }

        block_new = ClientBlock.objects.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewFAQ(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        faq = FAQ.objects.get(id=1)
        blocks_list = []
        for i in faq.block.all():
            blocks_list.append({
                'id': i.id,
                'title': i.title,
                'description': i.description,
            })

        data = {
            'name': faq.name,
            'blocks': blocks_list,
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewFAQBlockById(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = FAQBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'title': block.title,
            'description': block.description,
        }

        return JsonResponse(data)

    def put(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = FAQBlock.objects.get(id=block_id)
        put_body = json.loads(request.body)
        block.title = put_body.get('title')
        block.description = put_body.get('description')
        block.save()

        data = {
            'message': f'Block with id: {block_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = FAQBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostFAQBlock(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)

        block_data = {
            'title': put_body.get('title'),
            'description': put_body.get('description'),
        }

        block_new = FAQBlock.objects.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewBlog(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.all()
        blocks_data = []
        for i in blogs:
            for j in i.block.all():
                blocks_data.append({
                    'id': j.id,
                    'name': j.title,
                    'description': j.description,
                    'previewimage': j.image.url,
                    'image id': j.image.public_id,
                    'content': j.content,
                })
            data = {
                'name': i.name,
                'blocks': blocks_data,
            }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewBlogBlockById(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = BlogBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'title': block.title,
            'description': block.description,
            'previewimage': block.image.url,
            'image id': block.image.public_id,
            'content': block.content,
        }

        return JsonResponse(data)

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        block_id = put_body.get('id')
        block = BlogBlock.objects.get(id=block_id)
        block.title = put_body.get('title')
        block.description = put_body.get('description')
        block.image = img
        block.content = put_body.get('content')
        block.save()

        data = {
            'message': f'Block with id: {block_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = BlogBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostBlogBlock(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image

        block_data = {
            'title': put_body.get('title'),
            'description': put_body.get('description'),
            'image': img,
            'content': put_body.get('content'),
        }

        block_new = BlogBlock.objects.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewIndustry(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        industry = Industries.objects.get(id=1)
        blocks_data = []
        type_data = []
        block_kost = 0
        for i in industry.type.all():
            for j in i.block.all():
                blocks_data.append({
                    'id': j.id,
                    'name': j.title,
                    'previewimage': j.image.url,
                    'image id': j.image.public_id,
                    'content': j.content,
                })
                block_kost += 1
            block_kost *= -1
            type_data.append({
                'id': i.id,
                'name': i.name,
                'blocks': blocks_data[block_kost:],
            })
            block_kost = 0

        data = {
            'name': industry.name,
            'types': type_data,
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewIndustryTypeById(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        type_id = put_body.get('id')
        industry_type = IndustryType.objects.get(id=type_id)
        blocks_data = []
        for i in industry_type.block.all():
            blocks_data.append({
                'id': i.id,
                'name': i.title,
                'previewimage': i.image.url,
                'image id': i.image.public_id,
                'content': i.content,
            })
        data = {
            'id': industry_type.id,
            'name': industry_type.name,
            'blocks': blocks_data,
        }

        return JsonResponse(data)

    def put(self, request):
        put_body = json.loads(request.body)
        type_id = put_body.get('id')
        industry_type = IndustryType.objects.get(id=type_id)
        put_body = json.loads(request.body)
        industry_type.name = put_body.get('name')
        industry_type.save()

        data = {
            'message': f'Type with id: {type_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        type_id = put_body.get('id')
        industry_type = IndustryType.objects.get(id=type_id)
        industry_type.delete()

        data = {
            'message': f'Block with id:{type_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostIndustryType(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)

        block_data = {
            'name': put_body.get('name')
        }

        block_new = IndustryType.objects.create(**block_data)

        data = {
            'message': 'New type has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewIndustryTypeBlockById(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = IndustriesBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'title': block.title,
            'previewimage': block.image.url,
            'image id': block.image.public_id,
            'content': block.content,
        }

        return JsonResponse(data)

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        block_id = put_body.get('id')
        block = IndustriesBlock.objects.get(id=block_id)
        block.title = put_body.get('title')
        block.image = img
        block.content = put_body.get('content')
        block.save()

        data = {
            'message': f'Block with id: {block_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = IndustriesBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostIndustryTypeBlock(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        type = IndustryType.objects.get(id=put_body.get('type id'))
        block_data = {
            'title': put_body.get('title'),
            'industry_type': type,
            'image': img,
            'content': put_body.get('content'),
        }

        block_new = IndustriesBlock.objects.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewService(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        service = Services.objects.get(id=1)
        blocks_data = []
        type_data = []
        block_kost = 0
        for i in service.type.all():
            for j in i.block.all():
                blocks_data.append({
                    'id': j.id,
                    'title': j.title,
                    'description': j.description,
                    'previewimage': j.image.url,
                    'image id': j.image.public_id,
                    'content': j.content,
                    'url': j.url,
                })
                block_kost += 1
            block_kost *= -1
            type_data.append({
                'id': i.id,
                'name': i.title,
                'blocks': blocks_data[block_kost:],
            })
            block_kost = 0

        data = {
            'name': service.name,
            'types': type_data,
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewServiceTypeById(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        type_id = put_body.get('id')
        service_type = ServiceType.objects.get(id=type_id)
        blocks_data = []
        for i in service_type.block.all():
            blocks_data.append({
                'id': i.id,
                'title': i.title,
                'description': i.description,
                'previewimage': i.image.url,
                'image id': i.image.public_id,
                'content': i.content,
                'url': i.url,
            })
        data = {
            'id': service_type.id,
            'title': service_type.title,
            'blocks': blocks_data,
        }

        return JsonResponse(data)

    def put(self, request):
        put_body = json.loads(request.body)
        type_id = put_body.get('id')
        service_type = IndustryType.objects.get(id=type_id)
        put_body = json.loads(request.body)
        service_type.title = put_body.get('title')
        service_type.save()

        data = {
            'message': f'Type with id: {type_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        type_id = put_body.get('id')
        service_type = ServiceType.objects.get(id=type_id)
        service_type.delete()

        data = {
            'message': f'Block with id:{type_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostServiceType(View):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        service = Services.objects.get(id=1)

        block_data = {
            'service': service,
            'title': put_body.get('title')
        }

        block_new = ServiceType.objects.create(**block_data)

        data = {
            'message': 'New type has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewServiceTypeBlockById(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = ServiceTypeBlock.objects.get(id=block_id)
        data = {
            'id': block.id,
            'title': block.title,
            'description': block.description,
            'previewimage': block.image.url,
            'image id': block.image.public_id,
            'content': block.content,
            'url': block.url,
        }

        return JsonResponse(data)

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        block_id = put_body.get('id')
        block = ServiceTypeBlock.objects.get(id=block_id)
        block.title = put_body.get('title')
        block.image = img
        block.description = put_body.get('description')
        block.content = put_body.get('content')
        block.url = put_body.get('url')
        block.save()

        data = {
            'message': f'Block with id: {block_id} has been changed'
        }

        return JsonResponse(data)

    def delete(self, request):
        put_body = json.loads(request.body)
        block_id = put_body.get('id')
        block = ServiceTypeBlock.objects.get(id=block_id)
        block.delete()

        data = {
            'message': f'Block with id:{block_id} has been deleted'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class PostServiceTypeBlock(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        put_body = json.loads(request.body)
        images = Images.objects.all()
        for i in images:
            print(i.image.public_id)
            if i.image.public_id == put_body.get('image'):
                img = i.image
        type = ServiceType.objects.get(id=put_body.get('type id'))
        block_data = {
            'title': put_body.get('title'),
            'description': put_body.get('description'),
            'image': img,
            'content': put_body.get('content'),
            'url': put_body.get('url'),
            'service_type': type,
        }

        block_new = ServiceTypeBlock.objects.create(**block_data)
        data = {
            'message': 'New block has been created'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewLinks(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        links = Links.objects.all()
        links_list = []
        for i in links:
            links_list.append({
                'mail': i.mail,
                'facebook': i.facebook,
                'instagram': i.instagram,
            })
        data = {
            'links': links_list
        }
        return JsonResponse(data)

    def put(self, request):
        links = Links.objects.get(id=1)
        put_body = json.loads(request.body)
        links.mail = put_body.get('mail')
        links.instagram = put_body.get('instagram')
        links.facebook = put_body.get('facebook')

        data = {
            'message': f'Links have been changed'
        }

        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ViewTitle(View):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        title = Title.objects.get(id=1)
        data = {
            'text': title.text
        }

        return JsonResponse(data)

    def put(self, request):
        title = Title.objects.get(id=1)
        put_body = json.loads(request.body)
        title.text = put_body.get('text')

        data = {
            'message': f'Title text has been changed'
        }

        return JsonResponse(data)
