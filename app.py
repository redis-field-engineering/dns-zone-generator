from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View


app = Flask(
   __name__,
   static_url_path='/images',
   static_folder='images',
   )
bootstrap = Bootstrap()
SESSION_TYPE = 'redis'

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
         'host3-short': "ns2",
         'ip1': "10.1.1.1",
         'ip2': "10.1.1.2",
         'ip3': "10.1.1.3",
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
   mytemplate = '{}.html'.format(f['server'])

   # Add all the information to the current session
   session['zone_info'] = f
   return render_template(mytemplate, data = f)

if __name__ == '__main__':
   sess = Session(app)
   sess.init_app(app)
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=8080, host="0.0.0.0")
