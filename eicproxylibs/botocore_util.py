import sys
import botocore.session

from argparse import Namespace
from eicproxylibs import __version__ as CLI_VERSION

def get_session(profile_name=None, region=None):
    """
    Generates a botocore session with Managed SSH CLI set as the user agent
    :param profile_name: The name of a profile to use.  If not given, then the \
        default profile is used.
    :type profile_name: string
    :param region: An AWS region name to set as the default for the Botocore session
    :type region: string
    :return: A Botocore session object
    :rtype: botocore.session.Session
    """
    session = botocore.session.get_session()
    botocore_info = 'Botocore/{0}'.format(session.user_agent_version)
    if session.user_agent_extra:
        session.user_agent_extra += ' ' + botocore_info
    else:
        session.user_agent_extra = botocore_info
    session.user_agent_name = 'eicproxy'
    session.user_agent_version = CLI_VERSION
    """
    # Credential precedence:
    # 1. set user passed profile.
    # 2. set user passed region.
    # 3. let botocore handle the rest.
    """
    if profile_name:
        session.set_config_variable('profile', profile_name)
    if region is not None:
        session.set_config_variable('region', region)
    return session

def get_instance_data(session, instance_id):
    """
    Calls EC2 DescribeInstances API to get the DNS Names and IP addresses of the instance both Public and Private
    and also gets the Availability Zone of an instance

    :param session: A Botocore session to use to generate the EC2 client
    :type session: Botocore.session.Session
    :param instance_id: InstanceID of the instance
    :type instance_id: basestring
    :return: Namespace with Public DNS Name, Private DNS Name, Public IP, Private IP and Availability Zone
    :rtype: argparse.Namespace
    """

    try:
        client = session.create_client('ec2')
        instance_id = [instance_id]
        response = client.describe_instances(InstanceIds=instance_id)
        availability_zone = response['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
        try:
            public_dns_name = response['Reservations'][0]['Instances'][0]['PublicDnsName']
        except:
            public_dns_name = None
            pass
        try:
            private_dns_name = response['Reservations'][0]['Instances'][0]['PrivateDnsName']
        except:
            private_dns_name = None
            pass
        try:
            public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        except:
            public_ip = None
            pass
        try:
            private_ip = response['Reservations'][0]['Instances'][0]['PrivateIpAddress']
        except:
            private_ip = None
            pass
    except Exception as e:
        print(str(e))
        sys.exit(1)
    else:
        if len(availability_zone) == 0:
            print("Instance zone information not found")
            sys.exit(7)
        if not (public_dns_name or private_dns_name or public_ip or private_ip):
            print("No hostname or IPs found")
            sys.exit(8)
        else:
            instance_info = Namespace(public_dns_name=public_dns_name,
                                      private_dns_name=private_dns_name,
                                      public_ip=public_ip,
                                      private_ip=private_ip,
                                      availability_zone=availability_zone
                                      )

    return instance_info