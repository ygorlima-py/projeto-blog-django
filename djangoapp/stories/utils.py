from PIL import Image, ExifTags
from django.core.files.storage import default_storage
from .models import Story

def read_metadata(caminho: str):
    
    
    with default_storage.open(caminho, 'rb') as f:
        img = Image.open(f)
        
        info = {
                "formato": img.format,
                "modo": img.mode,
                "largura": img.width,
                "altura": img.height,
            }
        
        exif = img.getexif()
        for tag_id, valor in exif.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            info[tag] = valor
        
        # Dados em sub-IFDs (câmera, exposição, data original, etc.)
        for ifd_id in (ExifTags.IFD.Exif, ExifTags.IFD.GPSInfo):
            try:
                ifd = exif.get_ifd(ifd_id)
            except Exception:
                continue
            
            for tag_id, valor in ifd.items():
                nome = (ExifTags.GPSTAGS if ifd_id == ExifTags.IFD.GPSInfo else ExifTags.TAGS).get(tag_id, tag_id)
                info[nome] = valor

        return info


if __name__ == "__main__":
    read_metadata('stories/cover/20260125_152829.jpg')