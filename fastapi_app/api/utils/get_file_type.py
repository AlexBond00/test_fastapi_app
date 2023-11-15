from fastapi import UploadFile


async def get_file_type(file: UploadFile):
    """Get file type."""
    return file.content_type.split('/')[0]
