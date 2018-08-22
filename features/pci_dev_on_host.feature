Feature: SmartNIC as PCI device on the host

    Scenario: SmartNIC presents 2 HCAs
        Given arch is x86_64
        When execute `lspci -n -d15b3:a2d2:0200`
        Then have 2 records

    Scenario: SmartNIC presents NVMe
        Given arch is x86_64
        When execute `lspci -n -d15b3:b2d2:0108`
        Then have 1 record

    Scenario: BF is in "SmartNIC" mode
        Given mst service is loaded
        When  query mlxconfig -d /dev/mst/mt41682_pciconf0
         Then have INTERNAL_CPU_MODEL EMBEDDED_CPU(1)

    Scenario: RSHIM network interface to SmartNIC
        Given rshim_net module is loaded
         When interface name is tmfifo_net0
         Then state is UP
          And ipaddr is 192.168.100.1
          And mac is 00:1a:ca:ff:ff:02
          And driver is virtio_net
