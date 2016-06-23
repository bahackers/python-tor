Python TOR
==========

It's a simple Python software that show how use TOR as proxy to the connections
made for this app.

## Requirements

Have TOR installed as a service, you can install it following the command:

For Debian and Debian based:
```code
apt-get install tor
```

For Red Hat, CentOS or Fedora:
```code
dnf install tor
```

## Setting up

To run this example you must have Python 2.7.x installed.

I recommend use virtualenv to install the libraries and don't conflit with you environment.

I also recomendo you to keep you pip up to date, once you clone this repository and open it root directory, run the commands:

To be sure that pip is up to date:
```code
sudo pip install --upgrade pip
```

If you don't have virtualenv installed:
```code
pip install virtualenv
```

To create our virtual environment:
```code
virtualenv -p python2 .venv
```

Lets activate it:
```code
source .venv/bin/activate
```

Now we will install the dependencies
```code
pip install -r requirements.txt
```

Once the all dependencies are installed and the envonronment setted up we can run the app:
```code
python python_tor.py
```
