# -*- encoding=utf-8 -*-

__all__ = [
    'normalize',
    'normalizer',
    'UriNormalizer',
]

"""
URI normalization
"""

import idna # type: ignore
import re
import socket
import typing

from urllib.parse import (
    quote,
    unquote,
    urlparse,
    urlunparse
)


scheme_pattern = r'[a-zA-Z][a-zA-Z0-9+.-]*:'
ip4_addr_pattern = r'(?:0x[0-9a-fA-F]+|[0-9]+)(?:\.0x[0-9a-fA-F]+|[0-9]+){0,3}'


class UriNormalizer:
    """
    Implement URI normalization as specified by google

    https://developers.google.com/safe-browsing/v4/urls-hashing#canonicalization
    """
    def unquote_repeat(self, component: str) -> str:
        """
        repeatedly remove percent-quoting
        from an URL component
        """
        new = unquote(component, errors='strict')
        while new != component:
            component = new
            new = unquote(component, errors='strict')
        return component

    def normalize_host(self, host: str) -> str:
        """
        Normalize an URI hostname

        - remove percent quoting
        - remote port if present
        - remote trailing and leading dots
        - shorten sequences of two or more dots to a single dot
        - lower case the hostname
        - normalize IP hostnames into dotted-quad form
        - encode international hostnames into their punycode form
        """
        new_host = self.unquote_repeat(host)
        host_port = new_host.rsplit(':', 1)
        new_host = host_port[0]

        # strip leading and trailing dots
        new_host = new_host.strip('.')
        # remote repeated dots
        new_host = re.sub(r'\.{2,}', '.', new_host)
        # lowercase hostname
        new_host = new_host.lower()
        # if the hostname is an IP address, canonicalize the IP
        if re.match('^' + ip4_addr_pattern + '$', new_host):
            new_host = socket.inet_ntoa(socket.inet_aton(new_host))
        # international domain names are encoded into their
        # IDNA alabel form
        new_host = idna.encode(new_host).decode('ascii')
        # requote host
        new_host = quote(new_host, safe='.')
        return new_host

    def normalize_path(self, path: str) -> str:
        """
        Normalize URI path

        - remove percent quoting
        - perform '.' and '..' removal
        - replace an empty path by '/'
        """
        path = self.unquote_repeat(path)
        components = path.split('/')

        new_components: typing.List[str] = []
        for component in components:
            if component == '..' and new_components:
                del new_components[-1]
            elif component != '.':
                # append empty components only when not at the start
                # or the previous component is not empty.
                if component or (new_components and new_components[-1]):
                    new_components.append(component)

        path = '/'.join(new_components)
        if not path:
            path = '/'
        return quote(path, safe="!$&'()*+,;=/@-._~^")

    def normalize(self, uri: str) -> str:
        """
        perform URI normalization
        """
        new_uri = re.sub(r'[\t\r\n]+', '', uri)
        new_uri = re.sub(r'\s+$', '', new_uri)
        new_uri = re.sub(r'^\s+', '', new_uri)
        if not re.match('^' + scheme_pattern, new_uri):
            new_uri = 'http://' + new_uri

        scheme, netloc, path, params, query, fragment = urlparse(new_uri)
        netloc = self.normalize_host(netloc)
        path = self.normalize_path(path)
        new_uri = urlunparse([scheme, netloc, path, params, query, ''])
        return new_uri


normalizer = UriNormalizer()

normalize = normalizer.normalize
