from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class DocImage:

    def __init__(self, base_image):
        self.img = Image.open('assets/{}.png'.format(base_image))

    def return_image(self, img):
        img_io = BytesIO()
        img.save(img_io, 'PNG', quality=70)
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

    def gen_gcp(self, data):
        d1 = ImageDraw.Draw(self.img)
        myFont = ImageFont.truetype("assets/Amazon-Ember-Medium.ttf", 14)
        if data['record_type'] == "gcp_a":
            d1.text((290, 136), '{}.{}'.format(data['record'], data['fqdn']), font=myFont, fill =(0,0,0))
            d1.text((290, 430), data['ip_addrs'], font=myFont, fill =(0,0,0))
        else:
            d1.text((290, 136), data['fqdn'], font=myFont, fill =(0,0,0))
            d1.text((290, 430), '{}.{}'.format("ns1", data['fqdn']), font=myFont, fill =(0,0,0))
            d1.text((290, 500), '{}.{}'.format("ns2", data['fqdn']), font=myFont, fill =(0,0,0))
            d1.text((290, 570), '{}.{}'.format("ns3", data['fqdn']), font=myFont, fill =(0,0,0))
        return self.return_image(self.img)


    def gen_azure(self, data):
        d1 = ImageDraw.Draw(self.img)
        myFont = ImageFont.truetype("assets/Amazon-Ember-Medium.ttf", 14)
        if data['record_type'] == "azure_a":
            d1.text((15, 44), data['tld'], font=myFont, fill =(0,0,0))
            d1.text((26, 102), '{}.{}'.format(data['record'], data['prefix']), font=myFont, fill =(0,0,0))
            d1.text((259, 124), '.{}'.format(data['tld']), font=myFont, fill =(0,0,0))
            d1.text((35, 372), data['ip_addrs'], font=myFont, fill =(0,0,0))
        else:
            d1.text((20, 42), data['tld'], font=myFont, fill =(0,0,0))
            d1.text((30, 100), data['prefix'], font=myFont, fill =(0,0,0))
            d1.text((259, 124), '.{}'.format(data['tld']), font=myFont, fill =(0,0,0))
            d1.text((30, 318), '{}.{}'.format("ns1", data['prefix']), font=myFont, fill =(0,0,0))
            d1.text((30, 348), '{}.{}'.format("ns2", data['prefix']), font=myFont, fill =(0,0,0))
            d1.text((30, 380), '{}.{}'.format("ns3", data['prefix']), font=myFont, fill =(0,0,0))
        return self.return_image(self.img)
