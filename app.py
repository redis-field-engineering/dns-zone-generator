from flask import Flask, render_template, request, redirect, session, send_file
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from IPy import IP
from genimage import DocImage
from os import environ
import redis

app = Flask(
   __name__,
   static_url_path='/images',
   static_folder='images',
   )
bootstrap = Bootstrap()
SESSION_TYPE = 'redis'

# SESSION_REDIS format is redis://:[password]@[host_url]:[port]
if environ.get('SESSION_REDIS') is not None:
   SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))


app.config.from_object(__name__)


nav = Nav()
topbar = Navbar('',
    View('Zone Generator', 'index'),
    View('Troubleshooting Guide', 'troubleshooting'),
)
nav.register_element('top', topbar)

@app.route('/')
def index():
   zone_info = session.get('zone_info')
   if zone_info == None:
      zone_info = {
         'fqdn': "redis.example.com",
         'tld': "example.com",
         'host1-short': "ns1",
         'host2-short': "ns2",
         'host3-short': "ns3",
         'ip1': "10.1.1.1",
         'ip2': "10.1.1.2",
         'ip3': "10.1.1.3",
         'iptype': 'PRIVATE'
      }
   return render_template('index.html', zone_info = zone_info)

@app.route('/troubleshooting')
def troubleshooting():
   zone_info = session.get('zone_info')
   return render_template('troubleshooting.html', zone_info = zone_info)


@app.route('/generatezone', methods = ['POST'])
def generatezone():
   f = request.form.to_dict()
   tld = f['fqdn'].split('.')[1:]
   f['prefix'] = f['fqdn'].split('.')[0]
   f['tld'] = '.'.join(tld)
   f['host1-short'] = f['host1'].split('.')[0]
   f['host2-short'] = f['host2'].split('.')[0]
   f['host3-short'] = f['host3'].split('.')[0]
   try:
      f['iptype'] = IP(f['ip1']).iptype()
   except ValueError:
      return "<html> <body> <p>Incorrect IP addres format.</p><p>You will be redirected in 3 seconds</p> <script> var timer = setTimeout(function() { window.location='/' }, 3000); </script> </body> </html>"

   mytemplate = '{}.html'.format(f['server'])

   # Add all the information to the current session
   session['zone_info'] = f
   return render_template(mytemplate, data = f)

@app.route('/genimageroute53')
def genimageroute53():
   image_strings = {
      'route53A': 'A - Routes traffice to an IPv4 address..',
      'route53NS': 'NS - Name servers for a hosted zone',
   }

   data = {key:value for (key,value) in request.args.items()}
   data['record_string'] = image_strings[request.args.get('record_type')]
   data['ips'] = request.args.get('ip_addrs').split(',')

   img = DocImage(data['template'])
   return send_file(
      img.gen_route53(data),
      mimetype='image/png'
      )

@app.route('/genimagegcp')
def genimagegcp():
   data = {key:value for (key,value) in request.args.items()}
   data['ips'] = request.args.get('ip_addrs').split(',')
   img = DocImage(data['record_type'])
   return send_file(
      img.gen_gcp(data),
      mimetype='image/png'
   )

@app.route('/genimageazure')
def genimageazure():
   data = {key:value for (key,value) in request.args.items()}
   data['ips'] = request.args.get('ip_addrs').split(',')
   img = DocImage(data['record_type'])
   return send_file(
      img.gen_azure(data),
      mimetype='image/png'
   )


if __name__ == '__main__':
   sess = Session(app)
   sess.init_app(app)
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=8080, host="0.0.0.0")
