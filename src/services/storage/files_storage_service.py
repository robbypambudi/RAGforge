import os
import aiofiles
from src.constants import DOCUMENT_PATH

class FileStorageService:
    _relative_path = DOCUMENT_PATH
    
    def __init__(self) -> None:
        pass
    
    async def save(self, title, file):
        # Remove extension from file name
        if title.endswith('.pdf'):
            folderName = title[:-4]
        else:
            folderName = title
        
        # Full path to the folder
        folderPath = os.path.join(self._relative_path, folderName)
        
        # Check if folder exists
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        else:
            print(f"Folder {folderName} already exists")
            raise FileExistsError(f"Folder {folderName} already exists")
        
        # Save the file
        filePath = os.path.join(folderPath, file.filename)
        
        # Write the file content to the specified path
        async with aiofiles.open(filePath, 'wb') as f:
            await f.write(file.read())
            
        return filePath
    
    
        