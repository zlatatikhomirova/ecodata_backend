from dataclasses import asdict, dataclass
from typing import BinaryIO

from services.exceptions import DomainError
from storage.minio import BaseMinioRepo, MinioImageRepo


@dataclass
class FileDto:
    filename: str
    content_type: str
    file: BinaryIO
    size: int


class S3Service:
    
    def __init__(self, s3_repo: BaseMinioRepo | MinioImageRepo):
        self.s3_repo = s3_repo
        
    async def check_image(self, image_id: str | None):
        if image_id is None:
            return False
        return True
        
    async def upload(self, file: FileDto):
        await self.check_image(file.filename)
        identity = await self.s3_repo.upload(**asdict(file))
        return identity