
def resize(i):

    # stolen from https://stackoverflow.com/questions/623698/resize-image-on-save

    import StringIO
    from PIL import Image, ImageOps
    import os
    import hashlib
    from django.core.files import File
    # read image from InMemoryUploadedFile
    image_str = ""
    for c in i.chunks():
        image_str += c

    # create PIL Image instance
    imagefile  = StringIO.StringIO(image_str)
    image = Image.open(imagefile)

    # if not RGB, convert
    if image.mode not in ("L", "RGB"):
        image = image.convert("RGB")

    #define file output dimensions (ex 60x60)
    x = 1024
    y = 1024

    #get orginal image ratio
    img_ratio = float(image.size[0]) / image.size[1]

    # resize but constrain proportions?
    if x==0.0:
        x = y * img_ratio
    elif y==0.0:
        y = x / img_ratio

    # output file ratio
    resize_ratio = float(x) / y
    x = int(x); y = int(y)

    # get output with and height to do the first crop
    if(img_ratio > resize_ratio):
        output_width = x * image.size[1] / y
        output_height = image.size[1]
        originX = image.size[0] / 2 - output_width / 2
        originY = 0
    else:
        output_width = image.size[0]
        output_height = y * image.size[0] / x
        originX = 0
        originY = image.size[1] / 2 - output_height / 2

    # disableing crop
    # cropBox = (originX, originY, originX + output_width, originY + output_height)
    # image = image.crop(cropBox)

    # resize (doing a thumb)
    image.thumbnail([x, y], Image.ANTIALIAS)

    # re-initialize imageFile and set a hash (unique filename)
    imagefile = StringIO.StringIO()
    filename = hashlib.md5(imagefile.getvalue()).hexdigest()+'.jpg'

    #save to disk
    imagefile = open(os.path.join('/tmp',filename), 'w')
    image.save(imagefile,'JPEG', quality=90)
    imagefile = open(os.path.join('/tmp',filename), 'r')
    content = File(imagefile)

    return filename, content
