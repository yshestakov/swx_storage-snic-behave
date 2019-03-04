# swx_storage-snic-behave
Kind of acceptance tests of SmartNIC written in behave / python

## Behave tutorial

https://behave.readthedocs.io/en/latest/tutorial.html

## Installation of behave
### on Ubuntu

    apt-get -y install python3-behave

### on RHEL7

    yum -y install python2-behave

## How to run

Run all schenarious in the project

    $ sudo behave

    Feature: SmartNIC as PCI device on the host # features/pci_dev_on_host.feature:1

      Scenario: RSHIM network interface to SmartNIC  # features/pci_dev_on_host.feature:18
        Given rshim_net module is loaded             # features/steps/pci_dev_on_host.py:63 0.001s
        When interface name is tmfifo_net0           # features/steps/pci_dev_on_host.py:73 0.005s
        Then state is UP                             # features/steps/pci_dev_on_host.py:89 0.001s
        And ipaddr is 192.168.100.1                  # features/steps/pci_dev_on_host.py:97 0.001s
        And mac is 00:1a:ca:ff:ff:02                 # features/steps/pci_dev_on_host.py:104 0.001s
        And driver is virtio_net                     # features/steps/pci_dev_on_host.py:112 0.004s


Run only slow scenarios:

    $ sudo behave --tags=slow

Run all scenarios except of slow one

    $ sudo behave --tags=-slow

    Feature: SmartNIC as PCI device on the host # features/pci_dev_on_host.feature:1

      Scenario: SmartNIC presents 2 HCAs         # features/pci_dev_on_host.feature:3
        Given arch is x86_64                     # features/steps/pci_dev_on_host.py:8 0.000s
        When execute `lspci -n -d15b3:a2d2:0200` # features/steps/pci_dev_on_host.py:14 0.022s
        Then have 2 records                      # features/steps/pci_dev_on_host.py:19 0.000s

      Scenario: SmartNIC presents NVMe           # features/pci_dev_on_host.feature:8
        Given arch is x86_64                     # features/steps/pci_dev_on_host.py:8 0.000s
        When execute `lspci -n -d15b3:b2d2:0108` # features/steps/pci_dev_on_host.py:14 0.022s
        Then have 1 record                       # features/steps/pci_dev_on_host.py:19 0.000s
        When execute `lspci -n -d15b3:b2d2:0108` # features/steps/pci_dev_on_host.py:14 0.022s
        Then have 1 record                       # features/steps/pci_dev_on_host.py:19 0.000s

      @slow
      Scenario: BF is in "SmartNIC" mode                  # features/pci_dev_on_host.feature:14
        Given mst service is loaded                       # None
        When query mlxconfig -d /dev/mst/mt41682_pciconf0 # None
        Then have INTERNAL_CPU_MODEL EMBEDDED_CPU(1)      # None

      Scenario: RSHIM network interface to SmartNIC  # features/pci_dev_on_host.feature:19
        Given rshim_net module is loaded             # features/steps/pci_dev_on_host.py:63 0.001s
        When interface name is tmfifo_net0           # features/steps/pci_dev_on_host.py:73 0.004s
        Then state is UP                             # features/steps/pci_dev_on_host.py:89 0.001s
        And ipaddr is 192.168.100.1                  # features/steps/pci_dev_on_host.py:97 0.000s
        And mac is 00:1a:ca:ff:ff:02                 # features/steps/pci_dev_on_host.py:104 0.000s
        And driver is virtio_net                     # features/steps/pci_dev_on_host.py:112 0.004s

    Feature: showing off behave # features/tutorial.feature:1

      Scenario: run a simple test        # features/tutorial.feature:3
        Given we have behave installed   # features/steps/tutorial.py:3 0.000s
        When we implement a test         # features/steps/tutorial.py:7 0.000s
        Then behave will test it for us! # features/steps/tutorial.py:11 0.000s

    2 features passed, 0 failed, 0 skipped
    4 scenarios passed, 0 failed, 1 skipped
    15 steps passed, 0 failed, 3 skipped, 0 undefined
    Took 0m0.057s

## Intall dependencies 

for ViM python-mode

    apt-get -y install  python3-pyflakes python3-pylama python3-jedi
