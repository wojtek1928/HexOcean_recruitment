import uuid
from django.utils import timezone, timesince
from rest_framework import serializers
from easy_thumbnails.files import get_thumbnailer
from django.core.validators import FileExtensionValidator

from images_archive.models import Image, Tier


class TierSerializer(serializers.ModelSerializer):
    thumbnailSize = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='size')

    class Meta:
        model = Tier
        fields = ['thumbnailSize']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.ImageField(write_only=True, validators=[
        FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'jpe'])])

    class Meta:
        model = Image
        fields = ['id', 'file']

    def create(self, validated_data):
        return Image.objects.create(**validated_data)

    def to_representation(self, instance):
        if instance.owner.tier is not None:
            # Custom reprezsentation
            representation = super().to_representation(instance)

            # URI constant needed for generating links
            if self.context["view"].kwargs.get("id"):
                string_to_cut = str(self.context["view"].kwargs.get("id")) + \
                    '?t=' + self.context['request'].GET.get('t')

                URI = self.context['request'].build_absolute_uri().rstrip(
                    string_to_cut)
            else:
                URI = self.context['request'].build_absolute_uri()
            # link to orginal
            if instance.owner.tier.has_link_orginal_IMG:
                representation['Orginal'] = URI + instance.file.name

            # getting thmbnail sizes coresponding with Owner tier
            Tier = TierSerializer(instance.owner.tier, context=self.context)
            thumbnail_sizes = Tier.data.get('thumbnailSize')

            # rendering links to thumbnails
            if thumbnail_sizes:
                for size in thumbnail_sizes:
                    options = {'size': (0, size), 'crop': 'scale'}
                    thumb_url = get_thumbnailer(
                        instance.file).get_thumbnail(options).url

                    representation[f'thumbnail_{size}'] = URI + thumb_url[1:]

            # Expired links
            has_permission_exp_links = instance.owner.tier.has_expiring_links
            id_specified = self.context['view'].kwargs.get('id')
            expiration_time = self.context['request'].GET.get('t')

            if has_permission_exp_links and id_specified and expiration_time:
                # saving new token and expiration time. Expiration time from user is validated in view.
                instance.token = uuid.uuid4()
                instance.link_expiration_time = expiration_time
                instance.save()

                current_token = getattr(instance, 'token', None)
                # Generating link
                representation['Expiring link'] = URI + \
                    instance.file.name + '?token=' + str(current_token)

            elif instance.owner.tier.has_expiring_links:
                # Expiring link field shows only if owner has perrmission
                current_token = instance.token
                expiring_link_created_at = instance.expiring_link_created_at
                link_expiration_time = instance.link_expiration_time

                if current_token and expiring_link_created_at:
                    time_delta = (timezone.now() -
                                  expiring_link_created_at).total_seconds()
                    if time_delta <= link_expiration_time:
                        representation['Expiring link'] = URI + \
                            instance.file.name + '?token=' + str(current_token)
                        representation['Link expire in'] = instance.link_expiration_time-time_delta
                    else:
                        representation[
                            'Expiring link'] = f'To get an expiring link to this image, append `/{instance.id}?t=[time_in_seconds]`` to the address'

                else:
                    representation[
                        'Expiring link'] = f'To get an expiring link to this image, append `/{instance.id}?t=[time_in_seconds]` to the address'
            return representation

        return super().to_representation(instance)
