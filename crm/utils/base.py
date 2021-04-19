import datetime
import os
import uuid

from django.utils.encoding import (force_str, force_text)


def documents_upload_path(instance, filename: str) -> str:
    new_filename = 'documents/%Y/%m/%d/{uuid}/{file_name}'.format(uuid=uuid.uuid4(), file_name=filename)
    new_filename = force_str(new_filename)
    new_filename = datetime.datetime.now().strftime(new_filename)
    new_filename = force_text(new_filename)
    new_filename = os.path.normpath(new_filename)
    return new_filename


def images_upload_path(instance, filename: str) -> str:
    new_filename = 'images/%Y/%m/%d/{uuid}/{file_name}'.format(uuid=uuid.uuid4(), file_name=filename)
    new_filename = force_str(new_filename)
    new_filename = datetime.datetime.now().strftime(new_filename)
    new_filename = force_text(new_filename)
    new_filename = os.path.normpath(new_filename)
    return new_filename


__all__ = ('documents_upload_path', 'images_upload_path',)
