from blog_platform.celery import app
from mainAuth.models import User
import os

@app.task
def change_avatar(pk):

    from PIL import Image
    user = User.objects.get(pk=pk)
    size = 256, 256

    infile = user.image
    outfile = os.path.splitext(infile)[0] + ".png"
    if infile != outfile:
        im = Image.open(infile)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(outfile, "PNG")
