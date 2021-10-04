from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View


# From our local file

app = Flask(__name__)
bootstrap = Bootstrap()


nav = Nav()
topbar = Navbar('',
    View('Zone Generator', 'index'),
    View('Troubleshooting Guide', 'troubleshooting'),
)
nav.register_element('top', topbar)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/troubleshooting')
def troubleshooting():
   return render_template('troubleshooting.html')


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
   return render_template(mytemplate, data = f)
   #return f

if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.debug = True
   app.run(port=8080, host="0.0.0.0")
