"""
The MIT License (MIT)
Copyright (c) Datos IO, Inc. 2015.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import getpass
import argparse
from IPy import IP


def parse_input():
    # Let's get those arguments.
    parser = argparse.ArgumentParser(description='Simple keyless ssh setup, from node to given ips.')
    parser.add_argument('-u', '--user', default=getpass.getuser(), help='OS user of remote nodes. Default is current username.')
    parser.add_argument('-k', '--key', help='Key to access remote nodes. Optional.')
    parser.add_argument('-p', '--password', help='Key to access remote nodes. Optional.')  # TODO: (Aaron) Implement.
    parser.add_argument('-i', '--ips', default='ips', help='File that lists ips of remote cluster nodes. Override with manual ips set inside script.')
    parser.add_argument('--verbose', action='store_true', help='Verbose mode.')

    args = parser.parse_args()

    # Add '-i' to the key string for ssh purposes.
    if args.key:
        args.key = '-i %s' % args.key

    if args.password:
        import sshpass  # We keep the requirements to a minimum this way.
        pass

    return args


def parse_ips(cluster_ips):
    """
    Consumes ips as a comma separated string or a file with single ips or ip pairs per line and returns list of (pub, priv) ips.
    :param cluster_ips comma separated IP string or IP file to be parsed.
    :return: [(pub_1, priv_1), (pub_2, priv_2), ..., (pub_n, priv_n)].

    example string:

        <pub_1>,<pub_2>,...,<pub_n>
        <pub_1>,<priv_1>,<pub_2>,<priv_2>,...,<pub_n>,<priv_n>

        '10.1.2.3,10.1.2.4,10.1.2.5'
        '10.1.2.3,107.1.2.3,10.1.2.4,107.1.2.4'

    example IP file:

        #########################################################################
        # Public  Private
        10.1.2.3  107.1.2.3  # Most restricted IP (private) always second on line.
        10.1.2.4  107.1.2.4
        10.1.2.5  # If no public or private IP, only need one IP on line.
        #########################################################################
    """
    try:
        ip_strings = cluster_ips.split(',')

        if len(ip_strings) > 1:
            ips = []
            if ip_strings[0].split('.')[0] != ip_strings[1].split('.')[0]:  # Assume if they're different then pub, priv pairs.
                curr_ips = []
                for ip in ip_strings:
                    curr_ips.append(ip)
                    if len(curr_ips) == 2:
                        ips.append(tuple(curr_ips))
                        curr_ips = []
                if len(curr_ips) > 0:
                    curr_ips.append(curr_ips[0])
                    ips.append(tuple(curr_ips))
            else:
                ips = [(x, x) for x in cluster_ips.split(',')]
                IP(ips[0][0])  # Assume if first one is good ip, then argument not passed in as file, but string.
        else:
            ips = [(x, x) for x in cluster_ips.split(',')]
            IP(ips[0][0])  # Assume if first one is good ip, then argument passed in as string.

    except ValueError:
        with open(cluster_ips, 'r') as f:
            lines = f.readlines()

        ips = []
        for line in lines:
            line = line.split('#')[0]  # Allow for commenting in file.
            line = ' '.join(line.split()).replace('\n', '').strip()

            if line != '':
                ip_data = line.split()
                if len(ip_data) > 1:
                    pub, priv = ip_data
                else:
                    pub = priv = ip_data[0]  # If only 1 ip on line, use for both pub and priv ip.
                ips.append((pub, priv))

    return ips


def main():

    args = parse_input()
    ips = parse_ips(args.ips)
    print(ips)

    if not os.path.isfile('~/.ssh/id_rsa'):
        os.system("ssh-keygen -f ~/.ssh/id_rsa -t rsa -N ''")  # Generate key.

    # Put pub key on all remote hosts.
    for pub_ip, priv_ip in ips:
        cmd = ''' cat ~/.ssh/id_rsa.pub | ssh  %s -o "StrictHostKeyChecking no" %s@%s "mkdir -p /home/%s/.ssh && cat >>  /home/%s/.ssh/authorized_keys" ''' % (args.key, args.user, priv_ip, args.user, args.user)
        if args.verbose:
            print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    main()
