from django.db import models
from user.models import User
from PIL import Image
import io
from django.core.files.storage import default_storage as storage


class Group(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    info = models.TextField(max_length=300, blank=True, null=True)
    members = models.ManyToManyField(User, related_name='joined_groups')

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


def get_image_path(instance, filename):
    from os.path import join

    return join("profile_pics", instance.user.first_name, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_profile')
    user_info = models.TextField(max_length=300, blank=True, null=True)
    image = models.ImageField(default="default.jpg", upload_to=get_image_path)

    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format='JPEG')
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()
        super().save(*args, **kwargs)


def get_group_image_path(instance, filename):
    from os.path import join

    return join("group_profile_pics", instance.group.group_name, filename)


class GroupProfile(models.Model):
    group = models.OneToOneField(
        Group, on_delete=models.CASCADE, related_name="group_profile"
    )
    image = models.ImageField(
        default="default_group.jpg", upload_to=get_group_image_path
    )

    def __str__(self):
        return self.group.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.save(in_mem_file, format='JPEG')
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()
