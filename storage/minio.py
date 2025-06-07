from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
import re
from typing import BinaryIO

import imgspy
import aiohttp
from miniopy_async import Minio, S3Error
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class S3StorageSettings(BaseModel):
    endpoint: str = "localhost:9000"
    bucket_name: str = "minio-ecodata"
    access_key: str | None = "CP3AGtimn5NWAVGczxno"
    secret_key: str | None = "27m20zJTVC1wnYTrpxFe9OnrmIa2dM65mIKmjQa1"
    session_token: str | None = None
    secure: bool = True
    region: str | None = None
    
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )
    
    
_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")


@dataclass(frozen=True)
class ImageInfo:
    content_type: str
    width: int
    height: int


@dataclass(frozen=True)
class ImageDescr(ImageInfo):
    name: str
    url: str
    size: int
    created_at: datetime


class BaseMinioRepo:
    base_url = "/media/"
    
    def __init__(
        self, minio_settings: S3StorageSettings, session: aiohttp.ClientSession
    ):
        self.client = Minio(
            endpoint=minio_settings.endpoint,
            access_key=minio_settings.access_key,
            secret_key=minio_settings.secret_key,
            secure=False,
        )
        self.bucket_name = minio_settings.bucket_name
        self._session = session
        
    async def exists(self, image_id: str) -> bool:
        try:
            return bool(await self.client.stat_object(self.bucket_name, image_id))
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            raise
        
    @staticmethod
    def secure_filename(filename: str) -> str:
        for sep in os.path.sep, os.path.altsep:
            if sep:
                filename = filename.replace(sep, " ")

        normalized_filename = _filename_ascii_strip_re.sub("", "_".join(filename.split()))
        filename = str(normalized_filename).strip("._")
        return filename
        
    @staticmethod
    def _get_file_size(file: BinaryIO) -> int:
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0, os.SEEK_SET)
        return size
    
    async def download(self, image_id: str) -> bytes:
        response = await self.client.get_object(
            self.bucket_name, image_id, self.session
        )
        return await response.read()
    
    async def create_new_id(self, filename: str) -> str:
        identity = self.secure_filename(filename)
        stem = Path(identity).stem
        suffix = Path(identity).suffix
        counter = 0

        while await self.exists(identity):
            counter += 1
            identity = f"{stem}-{counter}{suffix}"
        return identity
    
    async def upload(
        self, filename: str, file: BinaryIO, content_type: str, size: int | None = None
    ) -> str:
        identity = await self.create_new_id(filename)
        if not size:
            size = self._get_file_size(file)
        await self.client.put_object(
            self.bucket_name,
            identity,
            file,
            length=size,
            content_type=content_type,
        )
        return identity
    
    
class MinioImageRepo(BaseMinioRepo):
    async def upload(
        self, filename: str, file: BinaryIO, size: int | None = None
    ) -> str:
        identity = await self.create_new_id(filename)
        if not size:
            size = self._get_file_size(file)
        img_info = self._get_image_info(file)
        await self.client.put_object(
            self.bucket_name,
            identity,
            file,
            length=size,
            content_type=img_info.content_type,
            metadata={"height": img_info.height, "width": img_info.width},
        )
        return identity
    
    @staticmethod
    def _get_image_info(file: BinaryIO) -> ImageInfo:
        info = imgspy.info(file)
        file.seek(0, os.SEEK_SET)
        type = {"jpg": "jpeg"}.get(info["type"], info["type"])
        return ImageInfo(
            content_type=f"image/{type}", width=info["width"], height=info["height"]
        )