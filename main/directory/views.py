from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Directory, ElementOfDirectory
from .serializers import DirectorySerializer, ElementOfDirectorySerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

paginator = PageNumberPagination()
paginator.page_size = 10


# Получение списка справочников
# Метод GET url api/directory/all/
@api_view(['GET'])
def directory_list(request):
    directories = Directory.objects.all()
    result_page = paginator.paginate_queryset(directories, request)
    serializer = DirectorySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# Получение Справочников по дате
# url api/directory/date/?date=Y-m-d
@api_view(['GET'])
def directory_date(request):
    date = request.query_params['date']

    list_of_directories = Directory.objects.filter(date__contains=date)
    if len(list_of_directories) == 0:
        return Response(data=f"Нет Справочников на {date}", status=status.HTTP_404_NOT_FOUND)

    result_page = paginator.paginate_queryset(list_of_directories, request)
    serializer = DirectorySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# Получение Элементов справочника по версии Справочника
# url api/directory/version/?version=Версия Справочника
@api_view(['GET'])
def elements_of_directory(request):
    version = request.query_params['version']
    try:
        directory_id = Directory.objects.get(version=version).id
    except Directory.DoesNotExist:
        return Response(data=f"Нет Элементов в Справочнике версии {version}", status=status.HTTP_404_NOT_FOUND)

    list_of_elements = ElementOfDirectory.objects.filter(dictionary=directory_id)
    result_page = paginator.paginate_queryset(list_of_elements, request)
    serializer = ElementOfDirectorySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# Получение элементов заданного справочника текущей версии
# Возвращает список Элементов Справочника последней версии (последний по дате)
# url api/directory/validate/?name=Название Справочника
@api_view(['GET'])
def elements_current_directory(request):
    name_of_dictionary = request.query_params['name']
    try:
        directory_name = Directory.objects.filter(name=name_of_dictionary).latest('date')
    except Directory.DoesNotExist:
        return Response(data=f"Нет совпадений", status=status.HTTP_404_NOT_FOUND)

    list_of_current_dictionary_elements = ElementOfDirectory.objects.filter(dictionary=directory_name.id)

    result_page = paginator.paginate_queryset(list_of_current_dictionary_elements, request)
    serializer = ElementOfDirectorySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# Валидация элемента заданного справочника по указанной версии
# Возвращает список Элементов справочника (если они есть в Справочнике) по указанной версии Справочника
# url api/directory/element/validate/?version=Версия Справочника&code=Код Элемента
@api_view(['GET'])
def validate_element(request):
    version_of_dictionary = request.query_params['version']
    code_of_element = request.query_params['code']

    try:
        directory_id_by_version = Directory.objects.get(version=version_of_dictionary).id

    except Directory.DoesNotExist:
        return HttpResponse(status=404)

    try:
        validate_element = ElementOfDirectory.objects.filter(
            Q(code=code_of_element) & Q(dictionary=directory_id_by_version))

    except ElementOfDirectory.DoesNotExist:
        return HttpResponse(status=404)

    result_page = paginator.paginate_queryset(validate_element, request)
    serializer = ElementOfDirectorySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# Валидация элементов заданного справочника текущей версии
# Возвращается список Элементов (если они есть в Справочнике) с последней датой Справочника
# url api/directory/current/validate/?name=Название Справочника&code=Код Элемента
@api_view(['GET'])
def validate_current_element(request):
    name_of_dictionary = request.query_params['name']
    code_of_element = request.query_params['code']

    try:
        directory_name_latest = Directory.objects.filter(name=name_of_dictionary).latest('date')

    except Directory.DoesNotExist:
        return HttpResponse(status=404)

    try:
        validate_current_element = ElementOfDirectory.objects.filter(
            Q(code=code_of_element) & Q(dictionary=directory_name_latest.id))

    except ElementOfDirectory.DoesNotExist:
        return HttpResponse(status=404)

    result_page = paginator.paginate_queryset(validate_current_element, request)
    serializer = ElementOfDirectorySerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
