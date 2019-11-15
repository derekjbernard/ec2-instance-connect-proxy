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

import sys
import argparse

from os import listdir, makedirs
from os.path import expanduser, isfile
from os.path import join as pathjoin

from eicproxylibs.EC2InstanceConnectCLI import EC2InstanceConnectCLI
from eicproxylibs.EC2InstanceConnectKey import EC2InstanceConnectKey
from eicproxylibs.EC2InstanceConnectCommand import EC2InstanceConnectCommand
from eicproxylibs.EC2InstanceConnectLogger import EC2InstanceConnectLogger
from eicproxylibs import mproxy_input_parser
from eicproxylibs import mproxy_key_utils
from eicproxylibs import key_utils
from eicproxylibs import sshconf

DEFAULT_INSTANCE = ''
DEFAULT_PROFILE = None

def main(program, mode):
    """
    Parses system arguments and sets defaults
    Calls `ssh` or `sftp` to SSH into the Instance or transfer files.

    :param program: Client program to be used for SSH/SFTP operations.
    :type program: basestring
    :param mode: Identifies either SSH/SFTP operation.
    :type mode: basestring
    """
    


    usage = ""
    if mode == "proxy":
        usage="""
            Used in ssh option "ProxyCommand" in ssh config or on command line
            $ `ssh i-a87ede98a69ea349a -o "ProxyCommand mproxy %r@%h:%p"`
            mproxy %r@%h:%p [-t instance_id] [-u profile] ([-z availability_zone] [-r region])|[--regions region-1 region-2] [--get-private-ip] [--use-tag-name]

            target                => [user@]instance_id | [user@]hostname
            [supported ssh flags] => [-l login_name] [-p port]
        """

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-r', '--region', action='store', help='AWS region', type=str, default='us-east-1', metavar='')
    parser.add_argument('-z', '--zone', action='store', help='Availability zone', type=str, metavar='')
    parser.add_argument('-u', '--profile', action='store', help='AWS Config Profile', type=str, default=DEFAULT_PROFILE, metavar='')
    parser.add_argument('-t', '--instance_id', action='store', help='EC2 Instance ID. Required if target is hostname', type=str, default=DEFAULT_INSTANCE, metavar='')
    parser.add_argument('-d', '--debug', action="store_true", help='Turn on debug logging')
    parser.add_argument('-k', '--public-key-file', action='store', type=argparse.FileType('r'),
                        help=f'Public key file to use for connection.')
    parser.add_argument('-g', '--generate-key-path', action='store', type=str,  )
    parser.add_argument('--use-private-ip', action='store_true', help=f'Use private IP even if public IP is available. private ip is used if no public IP is available.', default=False)
    parser.add_argument('--use-tag-name', action='store_true', help=f'Search for instance with Tag Name equal to the host instance_id parameter.', default=False)
    parser.add_argument('--resolve-hostname', action='store', type=str, help=f'Search for instance trying to resolve dns or ip hostname to aws instance id', default=None)
    parser.add_argument('--jumphosts', action='store', help='ssh proxy through jumphosts to destination, processed in order given', type=str, nargs='+' , metavar='')

    args = parser.parse_known_args()

    print(str(args), file=sys.stderr)

    logger = EC2InstanceConnectLogger(args[0].debug)


    try:
        instance_bundles, flags, program_command = mproxy_input_parser.parseargs(args, mode)
    except Exception as e:
        print(str(e))
        parser.print_help()
        sys.exit(1)

    """
    Handle keys:
    proxy doesn't use the keys but we need a public key to send to aws
    Choices:
        generate a key at a predifined path with generate_key_path arg
        define an existing public key to use with the public_key_file arg
    gernerate_key_path and public_key_file are mutually exclusive
    
    public_key_file defaults to first found: 
    ~/.ssh/id_(rsa|ed25519|ecdsa|dsa).pub
    """
    
    if args[0].generate_key_path is not None:
        cli_key = EC2InstanceConnectKey(logger.get_logger(),
                                        args[0].generate_key_path)
        public_key = cli_key.get_pub_key()
        private_key = cli_key.get_priv_key_file()
    elif args[0].public_key_file is not None:
        public_key = args[0].public_key_file.read()
    else:
        # Look for an acceptable default public key
        sshdir = pathjoin(expanduser('~'),'.ssh')
        # set of default keys in order of acceptance
        keytypes = ['id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa']
        keyfiles = []
        try:
            keyfiles = listdir(sshdir)
        except (FileNotFoundError):
            makedirs(sshdir, mode=0o600)
            cli_key = EC2InstanceConnectKey(logger.get_logger(),
                                            pathjoin(sshdir, 'id_rsa'))
            public_key = cli_key.get_pub_key()
            private_key = cli_key.get_priv_key_file()
        if len(keyfiles) > 0:
            # Find first acceptable default public key
            try:
                public_key_file = next(
                    keyfile for keytype
                    in keytypes for keyfile in keyfiles
                    if keyfile == '{0}.pub'.format(keytype))
            except (StopIteration):
                cli_key = EC2InstanceConnectKey(logger.get_logger(),
                                                pathjoin(sshdir, 'id_rsa'))
                public_key = cli_key.get_pub_key()
                private_key = cli_key.get_priv_key_file()
            
            try:
                with open(pathjoin(sshdir, public_key_file), 'r') as pbkf:
                    public_key = pbkf.read()
                    private_key = public_key_file.split('.pub')[0]
            except Exception as e:
                print('Failed with:\n' + str(e))
                sys.exit(1)
    
    cli_command = EC2InstanceConnectCommand(program, instance_bundles, private_key, flags, program_command, logger.get_logger())

    try:
        # TODO: Handling for if the '-i' flag is passed
        cli = EC2InstanceConnectCLI(instance_bundles, str(public_key), cli_command, logger.get_logger())
        cli.invoke_command()
    except Exception as e:
        print('Failed with:\n' + str(e))
        sys.exit(1)
