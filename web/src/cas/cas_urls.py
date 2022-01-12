#  CTF Platform by RSR, educational platform to try cyber-security challenges
#  Copyright (C) 2022 ENSEIRB-MATMECA, Bordeaux-INP, RSR formation since 2018
#  Supervised by Toufik Ahmed, tad@labri.fr
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
flask_cas.cas_urls

Functions for creating urls to access CAS.
"""

from urllib.parse import quote
from urllib.parse import urlencode
from urllib.parse import urljoin


def create_url(base, path=None, *query):
    """ Create a url.

    Creates a url by combining base, path, and the query's list of
    key/value pairs. Escaping is handled automatically. Any
    key/value pair with a value that is None is ignored.

    Keyword arguments:
    base -- The left most part of the url (ex. http://localhost:5000).
    path -- The path after the base (ex. /foo/bar).
    query -- A list of key value pairs (ex. [('key', 'value')]).

    Example usage:
    >>> create_url(
    ...     'http://localhost:5000',
    ...     'foo/bar',
    ...     ('key1', 'value'),
    ...     ('key2', None),     # Will not include None
    ...     ('url', 'https://example.com'),
    ... )
    'http://localhost:5000/foo/bar?key1=value&url=https%3A%2F%2Fexample.com'
    """
    url = base
    # Add the path to the url if it's not None.
    if path is not None:
        url = urljoin(url, quote(path))
    # Remove key/value pairs with None values.
    query = filter(lambda pair: pair[1] is not None, query)
    # Add the query string to the url
    url = urljoin(url, '?{0}'.format(urlencode(list(query))))
    return url


def create_cas_login_url(cas_url, cas_route, service, renew=None, gateway=None):
    """ Create a CAS login URL.

    Keyword arguments:
    cas_url -- The url to the CAS (ex. https://sso.pdx.edu)
    cas_route -- The route where the CAS lives on server (ex. /cas)
    service -- (ex.  http://localhost:5000/login)
    renew -- "true" or "false"
    gateway -- "true" or "false"

    Example usage:
    >>> create_cas_login_url(
    ...     'https://sso.pdx.edu',
    ...     '/cas',
    ...     'https://localhost:5000',
    ... )
    'https://sso.pdx.edu/cas?service=https%3A%2F%2Flocalhost%3A5000'
    """
    return create_url(
        cas_url,
        cas_route,
        ('service', service),
        ('renew', renew),
        ('gateway', gateway),
    )


def create_cas_logout_url(cas_url, cas_route, service=None):
    """ Create a CAS logout URL.

    Keyword arguments:
    cas_url -- The url to the CAS (ex. https://sso.pdx.edu)
    cas_route -- The route where the CAS lives on server (ex. /cas/logout)
    url -- (ex.  https://localhost:5000/login)

    Example usage:
    >>> create_cas_logout_url(
    ...     'https://sso.pdx.edu',
    ...     '/cas/logout',
    ...     'https://localhost:5000',
    ... )
    'https://sso.pdx.edu/cas/logout?service=https%3A%2F%2Flocalhost%3A5000'
    """
    return create_url(
        cas_url,
        cas_route,
        ('service', service),
    )


def create_cas_validate_url(cas_url, cas_route, service, ticket,
                            renew=None):
    """ Create a CAS validate URL.

    Keyword arguments:
    cas_url -- The url to the CAS (ex. https://sso.pdx.edu)
    cas_route -- The route where the CAS lives on server (ex. /cas/serviceValidate)
    service -- (ex.  https://localhost:5000/login)
    ticket -- (ex. 'ST-58274-x839euFek492ou832Eena7ee-cas')
    renew -- "true" or "false"

    Example usage:
    >>> create_cas_validate_url(
    ...     'https://sso.pdx.edu',
    ...     '/cas/serviceValidate',
    ...     'https://localhost:5000/login',
    ...     'ST-58274-x839euFek492ou832Eena7ee-cas'
    ... )
    'https://sso.pdx.edu/cas/serviceValidate?service=https%3A%2F%2Flocalhost%3A5000%2Flogin&ticket=ST-58274-x839euFek492ou832Eena7ee-cas'
    """
    return create_url(
        cas_url,
        cas_route,
        ('service', service),
        ('ticket', ticket),
        ('renew', renew),
    )
