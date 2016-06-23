import getpass
import requests
import socket
import socks
import stem
import sys
import time

from stem.control import Controller
from stem.connection import MissingPassword, PasswordAuthFailed, AuthenticationFailure

URL = u'https://duckduckgo.com/?q=my+ip&t=ffab&ia=answer'
PROXY_ADDRESS = u'127.0.0.1'
PROXY_PORT = 9050
PROXY_CONTROLLER_PORT = 9051


def get_tor_controller():
    try:
        controller = Controller.from_port(PROXY_ADDRESS, port=PROXY_CONTROLLER_PORT)
        controller.authenticate()
        return controller
    except stem.SocketError as err:
        print u'Unable to connect to tor on port %d: %s' % (PROXY_CONTROLLER_PORT, err)
        sys.exit(1)
    except MissingPassword:
        pw = getpass.getpass('Controller password: ')
        try:
            controller.authenticate(password=pw)
            return controller
        except PasswordAuthFailed:
            print u'Unable to authenticate, password is incorrect'
            sys.exit(1)
    except AuthenticationFailure as err:
        print u'Unable to authenticate: %s' % err
        sys.exit(1)
    except Exception as err:
        print u'Unhandle error: %s' % err
        sys.exit(1)


def extract_ip_from_response(text):
    ip_pos = text.find('Your IP address is')
    return text[ip_pos:(ip_pos + 34)]


def activate_proxy_tor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,
                          PROXY_ADDRESS,
                          PROXY_PORT)
    socket.socket = socks.socksocket

def do_example_request_over_tor():
    res = requests.get(URL)
    ip_got = extract_ip_from_response(res.text)

    print u'[*] %s' % ip_got


def main():
    tor_controller = get_tor_controller() # this should be before setting up the proxy

    activate_proxy_tor()
    do_example_request_over_tor()

    # TOR controller
    print u'[*] Tor is running version %s' % tor_controller.get_version()

    # that reload the TOR config, also the relays that you were using
    tor_controller.signal(stem.Signal.RELOAD)

    print u'[*] After reload TOR config'
    do_example_request_over_tor()

    tor_controller.close()


if __name__ == '__main__':
    main()
