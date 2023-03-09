from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response

from images_archive.models import Image

# A function that manages access to images


def media_access_check(request, path):
    access_granted = False
    user = request.user

    if user.is_authenticated:
        # First condition is for authenticated users
        if user.is_superuser:
            # Access for admins
            access_granted = True
        else:
            # Access for user if is owner(split needed for thumbnails)
            image = Image.objects.get(
                file__contains=path.split('.')[0], owner=user)
            if image:

                # Only ogrinal image path.split('.') has len less than 3 thumbnails always has more
                if len(path.split('.')) < 3:
                    if image.owner.tier.has_link_orginal_IMG:
                        access_granted = True
                else:
                    access_granted = True
    else:
        # Second condition is for unauthenticated users. It is checking link for right token.
        token = request.GET.get('token')

        def Token_vaidator(token):
            try:
                # An image is only returned if any image has this token
                return Image.objects.get(token=token)

            except:
                return None

        image = Token_vaidator(token)
        time_delta = (timezone.now() -
                      image.expiring_link_created_at).total_seconds()
        # Access is granted only if the time to expiration is not exceeded.
        if token and time_delta <= image.link_expiration_time:
            access_granted = True

    return access_granted


def expiring_link_create(view, min_time, max_time, id):
    # Get t value from GET
    expiration_time = view.request.GET.get('t')
    if id and expiration_time:
        # Working only when id and time are given
        if expiration_time.isdigit():
            # Transforming only numeric values to int
            expiration_time = int(expiration_time)

            if min_time <= expiration_time <= max_time:
                image = view.get_object()
                serializer = view.get_serializer(image)
                return Response(serializer.data)
            else:
                return Response({'detail': f'Invalid t (expiration time) value (must be between {min_time} and {max_time}) is `{expiration_time}`'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': f't(expiration time) must be number (int) between {min_time} and {max_time} is `{expiration_time}`'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': f'Wrong format: should be: /`id`?t=`expiration time`. The `expiration time` value must be between {min_time} and {max_time}.'},
                        status=status.HTTP_400_BAD_REQUEST)
