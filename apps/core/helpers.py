from typing import List
from dataclasses import dataclass
from django.core.mail import EmailMessage
from django.db.models import Model
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict
from apps.core.pagination import DefaultPagination
from apps.core.exceptions import DefaultException
import decouple

class Helpers:
    serializer_class: Serializer
    serializer_class_list: Serializer
    pagination_class: DefaultPagination = None
    page_size = 5


    def to_response(self, data, many=False, **kwargs):
        """
        Converts the given data to a response using the serializer class.

        Parameters:
            data (Any): The data to be converted to a response.
            many (bool, optional): Whether the data is a collection of objects. Defaults to False.

        Returns:
            Any: The converted response data.
        """
        serializer = self.serializer_class_list(data, many=many, **{"context": kwargs})
        if not self.pagination_class or kwargs.get("return_only_data", False):
            return serializer.data
        
        request = kwargs.get("request", None)
        if not request:
            raise DefaultException(
                detail="Requisição não informada.",
                code=HTTP_400_BAD_REQUEST,
            )
        
        paginator: DefaultPagination = self.pagination_class()
        paginator.page_size = self.page_size
        paginated_queryset = paginator.paginate_queryset(data, request)
        serializer = self.serializer_class_list(paginated_queryset, many=many, **{"context": kwargs})
        response_data = paginator.get_paginated_response(serializer.data, return_only_data=True)
        return response_data

    def validate(self, data: dict, instance: Model = None):
        """
        Validates the given data using the specified serializer class and optional instance.
        
        Parameters:
            data (dict): The data to be validated.
            instance (Model, optional): The instance to be validated.
        
        Returns:
            If an instance is provided, returns the serializer instance. 
            If no instance is provided, returns the validated data from the serializer.
        """
        serializer: Serializer
        if not data:
            raise DefaultException(
                detail="Data não informada.",
                code=HTTP_400_BAD_REQUEST,
            )
        if instance:
            serializer = self.serializer_class(
                data=data,
                instance=instance,
                partial=True,
            )
        else:
            serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            normalized_erros = self._normalize_serializer_erros(
                dict(serializer.errors) if type(serializer.errors) \
                    is not ReturnDict else serializer.errors
            )
            raise DefaultException(
                detail=normalized_erros,
                code=HTTP_400_BAD_REQUEST,
            )
        if instance:
            return serializer
        else:
            return serializer.validated_data

    def _prepare_execute(self, validated_data: dict) -> None:
        """
        Check if a record with the given data already exists in the repository.

        Args:
            validated_data (dict): The data to be checked.

        Raises:
            DefaultException: If a record with the given data already exists.

        Returns:
            None
        """
        exists = self.repository.search_by_data(data=validated_data).exists()
        if exists:
            raise DefaultException(
                detail="Já existe um registro com os dados informados.",
                code=HTTP_400_BAD_REQUEST,
            )

    def _normalize_serializer_erros(self, erros):
        normalized_erros = {}
        for erro in erros:
            if isinstance(erros[erro], list):
                for item in erros[erro]:
                    normalized_erros[erro] = str(item)
            elif isinstance(erros[erro], dict):
                for sub_erro in erros[erro]:
                    normalized_erros[erro + "." + sub_erro] = erros[erro][sub_erro]
            else:
                normalized_erros[erro] = str(erros[erro])
        return normalized_erros

    def _set_serializer_class_list(self, serializer_class_list: Serializer):
        if not serializer_class_list:
            raise DefaultException(
                detail="Classe de serialização não informada.",
                code=HTTP_400_BAD_REQUEST,
            )
        self.serializer_class_list = serializer_class_list


@dataclass()
class ResponseAPI:
    """
    Classe responsável pela execução da lógica de negócio
    com tratamento de erros e respostas dinâmicas tratadas
    pelas execções.

    repo: object - Classe responsável pela
    status: int  - Status de retorno da API. Ex: 200 (OK), 400 (bad_request)
    """

    repo: object
    status: int

    def list(self, **kwargs):
        try:
            response = self.repo.list(**kwargs)
            return Response(response, status=self.status)

        except Exception as e:
            print(e)
            return Response({"response": e.detail}, status=e.code)

    def retrieve(self, **kwargs):
        try:
            response = self.repo.retrieve(**kwargs)
            return Response(response, status=self.status)

        except Exception as e:
            print(e)
            return Response({"response": e.detail}, status=e.code)

    def create(self, **kwargs):
        try:
            response = self.repo.create(**kwargs)
            return Response(response, status=self.status)

        except Exception as e:
            print(str(e))
            return Response({"response": str(e)}, status=e.code)

    def partial_update(self, **kwargs):
        try:
            kwargs
            response = self.repo.partial_update(**kwargs)
            return Response(response, status=self.status)

        except Exception as e:
            return Response({"response": e.detail}, status=e.code)

    def destroy(self, **kwargs):
        try:
            response = self.repo.destroy(**kwargs)
            return Response(response, status=self.status)

        except Exception as e:
            return Response({"response": e.detail}, status=e.code)


import requests

class GoogleBooksAPI:
    BASE_URL = decouple.config(
        "GOOGLE_BOOKS_API_URL",
        default="https://www.googleapis.com/books/v1/volumes"
    )

    def search_books(self, query):
        url = f"{self.BASE_URL}?q={query}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_book(self, book_id):
        url = f"{self.BASE_URL}/{book_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
