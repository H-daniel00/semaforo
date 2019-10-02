import os
import magic
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError

def validate_file_type(upload):
    # Make uploaded file accessible for analysis by saving in tmp
    tmp_path = 'tmp/%s' % upload.name[2:]
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
    # Get MIME type of file using python-magic and then delete
    file_type = magic.from_file(full_tmp_path, mime=True)
    default_storage.delete(tmp_path)
    # Raise validation error if uploaded file is not an acceptable form of media
    if file_type not in settings.FILE_TYPES:
        return False
    else:
        return True

def validate_file_type(upload):
    # Make uploaded file accessible for analysis by saving in tmp
    tmp_path = 'tmp/%s' % upload.name[2:]
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
    # Get MIME type of file using python-magic and then delete
    file_type = magic.from_file(full_tmp_path, mime=True)
    default_storage.delete(tmp_path)
    # Raise validation error if uploaded file is not an acceptable form of media
    print(file_type)
    if file_type not in settings.FILE_TYPES:
        return False
    else:
        return True

def validate_img_type(upload):
    # Make uploaded file accessible for analysis by saving in tmp
    tmp_path = 'tmp/%s' % upload.name[2:]
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
    # Get MIME type of file using python-magic and then delete
    file_type = magic.from_file(full_tmp_path, mime=True)
    default_storage.delete(tmp_path)
    # Raise validation error if uploaded file is not an acceptable form of media
    if file_type not in settings.IMAGE_TYPES:
        return False
    else:
        return True