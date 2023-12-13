import datetime
import json
import re
from io import BytesIO

import willow
from bs4 import BeautifulSoup
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wagtail import blocks
from wagtail.documents.models import Document
from wagtail.fields import StreamField
from wagtail.images.models import Image
from wagtail.models import Collection

from blog.models import ArticlePage
from navigation.blocks import HeaderNavigationBlock, HeaderNavigationLinkBlock, HeaderNavigationSubLinkBlock
from pages.blocks import HeaderMetaBlock
from pages.models import Header, SimplePage, ComplexPage, ComplexPageMaterial, ComplexPageTab


def add_complex_page_materials(page, page_collection, materials_dicts):
    material_collection = Collection.objects.filter(name='Материалы').child_of(page_collection).first()
    if material_collection is None:
        return
    for order, material_dict in enumerate(materials_dicts):
        document = Document.objects.filter(collection=material_collection, title=material_dict["file"]).first()
        if document is None:
            continue
        material = ComplexPageMaterial(
            sort_order=order,
            page=page,
            name=material_dict['name'],
            document=document
        )
        material.save()


def add_complex_page_tabs(page, page_collection, tabs_dicts):
    tabs_collection = Collection.objects.filter(name='Вкладки').child_of(page_collection).first()
    if tabs_collection is None:
        return
    for order, tab_dict in enumerate(tabs_dicts):
        tab_collection = tabs_collection.get_children().filter(name=tab_dict['name']).first()
        body = []
        for part in tab_dict['body']:
            if part[0] == 'rich_text':
                soup = BeautifulSoup(part[1], 'html.parser')
                while True:
                    a_document = soup.find('a-document')
                    if not a_document:
                        break
                    document_name = a_document['name']
                    document = Document.objects.filter(collection=tab_collection, title=document_name).first()
                    if document is None:
                        a_document.name = 'a'
                        continue
                    del a_document['name']
                    a_document['linktype'] = 'document'
                    a_document['id'] = f'{document.id}'
                    a_document.name = 'a'
                while True:
                    img = soup.find('interested-img')
                    if not img:
                        break
                    image = Image.objects.filter(collection=tab_collection, title=img['src'].split('/')[-1]).first()
                    if not image:
                        img.name = 'img'
                        continue
                    del img['src']
                    img['embedtype'] = 'image'
                    img['format'] = 'fullwidth'
                    img['id'] = f'{image.id}'
                    img.name = 'embed'
                body.append({'type': 'rich_text', 'value': str(soup)})
            elif part[0] == 'table':
                body.append({
                    'type': 'table',
                    'value': {
                        'cell': [],
                        'data': part[1],
                        'table_caption': '',
                        'first_col_is_header': False,
                        'first_row_is_table_header': False
                    }
                })
            elif part[0] == 'html':
                body.append({
                    'type': 'raw_html',
                    'value': part[1]
                })
        tab = ComplexPageTab(
            sort_order=order,
            page=page,
            name=tab_dict['name'],
            body=json.dumps(body)
        )
        tab.save()


@csrf_exempt
def init_complex_page(request: HttpRequest):
    page_dict = json.loads(request.body)
    root = SimplePage.objects.get(slug="pages").specific
    collection = Collection.objects.filter(
        name=page_dict['alias'],
    ).first()
    complex_page = ComplexPage(
        title=page_dict['name'],
        slug=page_dict['alias'],
        first_published_at=datetime.datetime.strptime(
            page_dict['published_at'],
            '%Y-%m-%dT%H:%M:%S'
        ) if page_dict['published_at'] else None,
        last_published_at=datetime.datetime.strptime(
            page_dict['published_at'],
            '%Y-%m-%dT%H:%M:%S'
        ) if page_dict['published_at'] else None,
        latest_revision_created_at=datetime.datetime.strptime(
            page_dict['created_at'],
            '%Y-%m-%dT%H:%M:%S'
        ) if page_dict['created_at'] else None
    )
    root.add_child(instance=complex_page)
    complex_page.save()
    add_complex_page_tabs(complex_page, collection, page_dict['tabs'])
    add_complex_page_materials(complex_page, collection, page_dict['materials'])


@csrf_exempt
def init_article(request: HttpRequest):
    # articles = ArticlePage.objects.all()
    # articles.delete()
    article_dict = json.loads(request.body)
    root = SimplePage.objects.get(slug="news").specific
    collection = Collection.objects.filter(
        name=article_dict['alias'],
    ).first()
    thumbnail = Image.objects.filter(
        collection=collection,
        title=article_dict['thumbnail']
    ).first()
    images_names = article_dict['images']
    images = Image.objects.filter(collection=collection, title__in=images_names).all()
    images_string = ''
    for image_name in images_names:
        try:
            image = list(filter(lambda img: img.title == image_name, images))[0]
            images_string += f'<p></p><embed alt =\"{image.title}\" embedtype=\"image\" format=\"fullwidth\" id=\"{image.id}\"/>'
        except Exception:
            pass
    article = ArticlePage(
        image=thumbnail,
        title=article_dict['name'],
        body=json.dumps([
          {'type': 'rich_text', 'value': re.sub('<img.*>', '', article_dict['body'], count=0, flags=0) + images_string}
        ]),
        slug=article_dict['alias'],
        first_published_at=datetime.datetime.strptime(
            article_dict['published_at'],
            '%Y-%m-%dT%H:%M:%S'
        ) if article_dict['published_at'] else None,
        last_published_at=datetime.datetime.strptime(
            article_dict['published_at'],
            '%Y-%m-%dT%H:%M:%S'
        ) if article_dict['published_at'] else None,
        latest_revision_created_at=datetime.datetime.strptime(
            article_dict['created_at'],
            '%Y-%m-%dT%H:%M:%S'
        ) if article_dict['created_at'] else None
    )
    root.add_child(instance=article)


def create_documents(collection, documents_dicts: list[dict], path_to_files: str):
    for document_dict in documents_dicts:
        document = Document.objects.filter(collection=collection, title=document_dict["name"]).first()
        if document is not None:
            continue
        file_path = f'{path_to_files}{document_dict["path"]}'
        document_file = File(open(file_path, 'rb'), name=document_dict['name'])
        document = Document.objects.create(collection=collection, title=document_dict["name"], file=document_file)
        document.save()


def create_images(collection, images_dicts: list[dict], path_to_files: str):
    for image_dict in images_dicts:
        image = Image.objects.filter(collection=collection, title=image_dict["name"]).first()
        if image is not None:
            continue
        file_path = f'{path_to_files}{image_dict["path"]}'
        image_file = ImageFile(open(file_path, 'rb'), name=image_dict['name'])
        image = Image.objects.create(collection=collection, title=image_dict["name"], file=image_file)
        image.save()


def create_collections(parent, collections_dicts: list[dict], path_to_files: str):
    for collection_dict in collections_dicts:
        collection = Collection.objects.filter(name=collection_dict['name']).child_of(parent).first()
        if collection is None:
            collection = parent.add_child(name=collection_dict['name'])
        create_images(collection, collection_dict['images'], path_to_files)
        create_documents(collection, collection_dict['documents'], path_to_files)
        if collection_dict['children']:
            create_collections(collection, collection_dict['children'], path_to_files)


@csrf_exempt
def init_collections(request: HttpRequest):
    data = json.loads(request.body)
    collections_dicts = data['collections']
    path_to_files = data['path_to_files']
    root = Collection.get_first_root_node()
    create_collections(root, collections_dicts, path_to_files)
