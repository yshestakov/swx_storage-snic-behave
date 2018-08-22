# swx_storage-snic-behave
Kind of acceptance tests of SmartNIC written in behave / python

## Behave tutorial

    https://behave.readthedocs.io/en/latest/tutorial.html

## Installation of behave
### on Ubuntu

    apt-get -y install python3-behave

## How to run

    $ behave

    Feature: SmartNIC as PCI device on the host # features/pci_dev_on_host.feature:1

      Scenario: RSHIM network interface to SmartNIC  # features/pci_dev_on_host.feature:18
        Given rshim_net module is loaded             # features/steps/pci_dev_on_host.py:63 0.001s
        When interface name is tmfifo_net0           # features/steps/pci_dev_on_host.py:73 0.005s
        Then state is UP                             # features/steps/pci_dev_on_host.py:89 0.001s
        And ipaddr is 192.168.100.1                  # features/steps/pci_dev_on_host.py:97 0.001s
        And mac is 00:1a:ca:ff:ff:02                 # features/steps/pci_dev_on_host.py:104 0.001s
        And driver is virtio_net                     # features/steps/pci_dev_on_host.py:112 0.004s


## Intall dependencies 

for ViM python-mode

    apt-get -y install  python3-pyflakes python3-pylama python3-jedi
