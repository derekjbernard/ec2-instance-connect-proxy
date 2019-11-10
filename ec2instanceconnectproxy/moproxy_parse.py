# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import re
import socket

INSTANCE_ID_RE = re.compile("i-[a-f0-9]+")
UNIX_USER_RE_STR = '[a-z_][a-z0-9_-]{0,31}'
UNIX_USER_RE = re.compile(UNIX_USER_RE_STR)
TCP_PORT_RE_STR = '()([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5])'
TCP_PORT_RE = re.compile(f'^{TCP_PORT_RE_STR}$')
HOSTNAME_CHR_MAX_RE_STR = '.{0,255}'
CONNECTION_STRING_RE = re.compile(f'^{UNIX_USER_RE_STR}@{HOSTNAME_CHR_MAX_RE_STR}:{TCP_PORT_RE_STR}$')

def connection_str(connection_string=None):

    """
    Parses the connection string composed of User@HostName:Port passed from ssh into eicproxy.

    :param connection_string: A string formmated 'User@HostName:Port'
    :type connection_string: string
    :param jumphost
    :return: dict containing at least os_user, host_token, host_token_type, ssh_port. host_token_type will be one of private_ip,public_ip,
    :rtype: conection_dict: dict
    """
    connection_dict = dict()

    if _is_valid_connection_str(connection_string):
        os_user = connection_string.split('@')[0]
        host_token = connection_string.split('@')[1].split(':')[0]
        ssh_port = connection_string.split('@')[1].split(':')[1]
    else:
        raise ValueError(f'eicproxy recieved invalid conection string: {connection_string}')

    if _is_valid_instance_id(host_token):
        host_token_type = instance_id
    elif _is_valid_ipv4_address(host_token):
        
    if len(args) < 2:
        raise AssertionError('Missing target')
    if len(args[1]) < 1:
        raise AssertionError('Missing target')

    """
    Our flags.  As these are via argparse they're free.
    Instance details are a bit weird.  Since the instance ID can either be the actual "host" or a flag we have to group it.
    We do this with an "instance bundle" dict.
    Note we don't load the actual instance DNS/IP/ID here - that comes later.
    """
    instance_bundles = [
        {
            'profile': args[0].profile,
            'instance_id': args[0].instance_id,
            'region': args[0].region,
            'zone': args[0].zone
        }
    ]

    return instance_bundles, flags, command
    
def _is_valid_connection_str(connection_string=None):
    """
    Validate if connection_str can be parsed
    """
    return CONNECTION_STRING_RE.match(connection_string) is not None

def _is_valid_instance_id(instance_id):
    """
    For supported modes ensure that instance_id exists.
    """
    return INSTANCE_ID_RE.match(instance_id) is not None

def _is_valid_username(username):
    """
    Validates if the provided username is a valid UNIX username

    :param username: username to validate
    :type username: basestring
    :return: Whether the given username is a valid UNIX username
    :rtype: bool
    """
    return UNIX_USER_RE.match(username) is not None


def _is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError: # inet_pton is not available
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:
        return False

    return True


def _is_valid_ipv6_address(address):
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True

def _is_valid_dns_hostname(hostname):
        """
    Validates if the provided "hostname" is a valid DNS name or IP address

    :param hostname: FQDN to validate
    :type hostname: basestring
    :return: Whether the given hostname is a valid DNS name or IP address
    :rtype: bool
    """
    if not hostname:
        return False

    # Check if it's a valid DNS name

    if hostname[-1] == '.':
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    if len(hostname) < 1 or len(hostname) > 253: # Technically 255 octets but 2 are used for encoding
        return False

    labels = hostname.split(".")

    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    allowed = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(label) for label in labels)

def _is_valid_target(hostname):
    """
    Validates if the provided "hostname" is a valid DNS name or IP address

    :param hostname: FQDN to validate
    :type hostname: basestring
    :return: Whether the given hostname is a valid DNS name or IP address
    :rtype: bool
    """
    if not hostname:
        return False

    # Check if it's a valid IP
    if _is_valid_ipv4_address(hostname) or _is_valid_ipv6_address(hostname):
        return True

    # Check if it's a valid DNS name
