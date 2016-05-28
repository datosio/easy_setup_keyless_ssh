# Easy Setup Keyless SSH
==========
by Datos IO
<http://www.datos.io>

Introduction
------------
Easy Setup Keyless SSH to one or multiple remote nodes.

Requirements
------------
##### System Libraries:
* Python 2.6+

##### Python Libraries: 
* IPy

Usage
-----
```
python setup_keyless_ssh.py -u <user> -p <pass> -i 10.0.1.10,10.0.1.11
```

optional arguments:
```
  -h, --help            show this help message and exit
  -u USER, --user USER  OS user of remote nodes. Default is current username.
  -k KEY, --key KEY     Key to access remote nodes. Optional.
  -p PASSWORD, --password PASSWORD
                        Key to access remote nodes. Optional.
  -i IPS, --ips IPS     File that lists ips of remote cluster nodes. Override
                        with manual ips set inside script.
  --verbose             Verbose mode.
```

Downloads
---------

Source code is available at <https://github.com/datosio/easy_setup_keyless_ssh>.

License
-------

The Easy Setup Cassandra code is distributed under the MIT License. <https://opensource.org/licenses/MIT>


Version History
---------------

Version 1.0 - June 7, 2016

* Initial release.