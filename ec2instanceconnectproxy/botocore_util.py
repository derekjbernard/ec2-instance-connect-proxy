import botocore.session
from ec2instanceconnectproxy import __version__ as CLI_VERSION

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
    session.user_agent_name = 'ec2-instance-connect-proxy'
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