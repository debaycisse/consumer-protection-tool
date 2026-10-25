from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from apps.consumer_protection.views.utils import CommonViewAttributes
from apps.consumer_protection.permissions.owner_permission import (
    IsItemOwner,
    IsAProducer,
)
from apps.consumer_protection.models.items import Items
from apps.consumer_protection.serializers.items_serializer import (
    ItemsSerializer,
)


class ItemListCreateView(CommonViewAttributes, APIView):
    """
    View to process list and create request for item resource

    Requires an authentication token
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsAProducer]

    def get(self, request, format=None):
        item_objects = Items.objects.select_related("producer_id")

        items_serializer = ItemsSerializer(item_objects, many=True)

        response_data = {"data": items_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        new_item_object = Items.objects.create(**request_data)

        # To ensure only producer can create an item
        self.check_object_permissions(request, new_item_object)

        item_serializer = ItemsSerializer(data=new_item_object)
        item_serializer.is_valid(raise_exception=True)
        item_serializer.save(producer_id=request.user)

        response_data = {"data": item_serializer.data}

        return Response(response_data, status=status.HTTP_201_CREATED)


class ItemRetrieveUpdateDestroyView(CommonViewAttributes, APIView):
    """
    View to process retrieve, update, and delete requests
    for an item resource

    Requires an authentication token
    """

    permission_classes = [IsAuthenticatedOrReadOnly, IsItemOwner]

    def get_object(self, item_id):
        return Items.objects.get(item_id=item_id)

    def get(self, request, item_id=None, format=None):
        item_object = self.get_object(item_id=item_id)

        item_serializer = ItemsSerializer(item_object)

        response_data = {"data": item_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, item_id=None, format=None):
        item_object = self.get_object(item_id=item_id)
        name = request.data.get("name", item_object.name)
        category = request.data.get("category", item_object.category)
        data = {"name": name, "category": category}

        self.check_object_permissions(request, item_object)

        item_serializer = ItemsSerializer(item_object, data=data)
        item_serializer.is_valid(raise_exception=True)
        item_serializer.save()

        response_data = {"data": item_serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, item_id=None, format=None):
        item_object = self.get_object(item_id=item_id)

        self.check_object_permissions(request, item_object)

        item_object.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
