import getpass
import requests
import socket
import socks
import sys
import time

from stem.control import Controller

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
        print u'Unable to connect to tor on port 9051: %s' % err
        sys.exit(1)
    except stem.connection.MissingPassword:
        pw = getpass.getpass('Controller password: ')
        try:
            controller.authenticate(password=pw)
        except stem.connection.PasswordAuthFailed:
            print u'Unable to authenticate, password is incorrect'
            sys.exit(1)
    except stem.connection.AuthenticationFailure as err:
        print u'Unable to authenticate: %s' % err
        sys.exit(1)


def extract_ip_from_response(text):
    ip_pos = text.find('Your IP address is')
    return text[ip_pos:(ip_pos + 34)]


def activate_proxy_tor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,
                          PROXY_ADDRESS,
                          PROXY_PORT)
    socket.socket = socks.socksocket


def main():
    # activate_proxy_tor()
    res = requests.get(URL)
    ip_got = extract_ip_from_response(res.text)

    print u'[*] %s' % ip_got

    # TOR controller

    # tor_controller = get_tor_controller()
    # print u'Tor is running version %s' % tor_controller.get_version()
    # tor_controller.close()


if __name__ == '__main__':
    main()
