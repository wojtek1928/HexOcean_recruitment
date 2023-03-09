from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator


# A model that defines the Tier, i.e. permissions for users
class Tier(models.Model):
    name = models.CharField(max_length=50)
    has_link_orginal_IMG = models.BooleanField(default=False)
    has_expiring_links = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


# A model containing the possible sizes of miniatures for a given tier
class ThumbnailSize(models.Model):
    tier = models.ForeignKey(Tier, related_name='thumbnailSize',
                             on_delete=models.CASCADE)
    size = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.size)


# A model that extends the default user model with Tier
class CustomUser(AbstractUser):
    # null=True, needed for superuser creation
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True)


# A model for storing original images
class Image(models.Model):
    file = models.ImageField(upload_to='images/', validators=[
                             FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'jpe'])])

    owner = models.ForeignKey(
        CustomUser, related_name='images', on_delete=models.CASCADE)

    token = models.UUIDField(blank=True, null=True)

    link_expiration_time = models.PositiveBigIntegerField(blank=True, null=True, validators=[
        MinValueValidator(300), MaxValueValidator(30000)])

    expiring_link_created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) -> str:
        return self.file.name
