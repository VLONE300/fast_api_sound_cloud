import os
from fastapi import UploadFile, HTTPException
import aiofiles


class FileManager:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        os.makedirs(self.base_directory, exist_ok=True)

    async def save_file(self, file: UploadFile, file_path: str) -> None:
        try:
            async with aiofiles.open(file_path, 'wb') as out_file:
                while content := await file.read(1024):  # Читаем файл порциями
                    await out_file.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    async def get_file(self, file_path: str) -> bytes:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        try:
            async with aiofiles.open(file_path, 'rb') as file:
                return await file.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not read file: {str(e)}")


# Инициализация фасада с базовой директорией для хранения файлов
FILE_MANAGER = FileManager(base_directory="static/songs")
