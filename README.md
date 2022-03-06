eicproxy - An AWS EC2 Instance Connect (EIC) enabled ssh ProxyCommand utility.

[EC2 Instance Connect]:https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Connect-using-EC2-Instance-Connect.html (EIC) grants ssh access to ec2 instances using aws credentials.

eicproxy utility provides the following features:
    * Brokers ec2 ssh access using AWS credentials with EIC.
    * Uses ec2 instance id or tag Name as hostnames.
    * supports bastion / jump hosts
    * works with ssh based tools like:
        * ansible
        * rsync
        * scp
        * sftp
        * ssh
        * autossh

Usage examples:
ad-hoc via command line ssh options:

`ssh ec2-user@i-87ad9e7f9ed90a8 -o "ProxyCommand eicproxy %r@%h:%p"`

Using ssh_config (Recommended):
Example `~/.ssh/config`

```bash
# Use a friendly alias for your ec2 bastion
Host My-Bastion
    Hostname <ec2 instance id>
    User ec2-user
    Port 22
    ProxyCommand eicproxy %r@%h:%p

Host My-Internal-DB
    Hostname <ec2 instance id>
    User ec2-user
    Port 22
    ProxyCommand eicproxy %r@%h:%p --use-private-ip --jumphost My-Bastion

Host My-Public-Web
    Hostname <ec2 instance id>
    User ec2-user
    Port 22
    ProxyCommand eicproxy %r@%h:%p

Host Dev-Public-Web
    Hostname <ec2 instance id>
    User ec2-user
    Port 22
    ProxyCommand eicproxy %r@%h:%p --profile dev-aws-account

Host i-* #Use eicproxy for all hostnames starting with i- 
    User ec2-user
    Port 22
    ProxyCommand eicproxy %r@%h:%p --regions us-east-1 us-east-2 us-west-1

# hack to specify custom named aws profile with instance id
Host dev-aws-profile-i-*
    ProxyCommand host=%h; eicproxy %r@${host#dev\-aws\-account\-}:%p --profile ${host%\-i*}

# hack to use tagName
Host awstn-*
    ProxyCommand tagname=%h; eicproxy %r@${tagname#awstn\-}:%p --use-tag-name
```