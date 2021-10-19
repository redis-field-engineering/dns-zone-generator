from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class DocImage:

    def __init__(self, base_image):
        self.img = Image.open('assets/{}.png'.format(base_image))

    def return_image(self, img):
        img_io = BytesIO()
        img.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        return img_io

    def gen_route53(self, data):
        d1 = ImageDraw.Draw(self.img)
        myFont = ImageFont.truetype("assets/Amazon-Ember-Medium.ttf", 14)
        d1.text((286, 62), data['tld'], font=myFont, fill =(0,115,187))
        d1.text((111, 259), data['record'], font=myFont, fill =(0,0,0))
        d1.text((267, 259), '.{}'.format(data['tld']), font=myFont, fill =(0,0,0))
        d1.text((464, 259), data['record_string'], font=myFont, fill =(0,0,0))
        ypos = 259
        for ip in data['ips']:
            d1.text((819, ypos), ip, font=myFont, fill =(0,0,0))
            ypos += 15
        return self.return_image(self.img)
