from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from django.http.response import FileResponse

from images_archive.models import Image
from .serializer import ImageSerializer
from .permissions import media_access_check, expiring_link_create


# View for images displaying
@api_view()
def media_access(request, image_name):

    access_granted = media_access_check(request, image_name)

    if access_granted:
        # path to response image needs be witout first / sign
        image_path = request.path_info
        response = FileResponse(
            open(image_path[1:], 'rb'))
        return response
    else:
        return Response({'detail': 'Not authorized to access this media'}, status=status.HTTP_403_FORBIDDEN)


# View for listing images
class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        images = self.get_queryset()
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Expirining link view
class ImageExpiringLink(generics.RetrieveAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    def get(self, request, id):
        # Protection against providing incorrect data: try-except
        try:
            if Image.objects.get(pk=id, owner=self.request.user).owner.tier.has_expiring_links:
                return expiring_link_create(view=self, min_time=300, max_time=30000, id=id)
            else:
                return Response({'detail': 'You can not generate expiring links'}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'detail': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)
