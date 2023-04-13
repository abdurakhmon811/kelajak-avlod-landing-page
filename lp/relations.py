from django.db import models


class SocialMedia(models.Model):
    """
    A model for handling social media for contact.
    """

    class Meta:

        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'
    
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='images')
    link = models.CharField(max_length=300, null=True)

    objects = models.Manager()

    def __str__(self) -> str:

        return self.name
