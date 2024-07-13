import cloudinary.uploader

def upload_avatar(file):
    result = cloudinary.uploader.upload(file)
    return result["url"]
