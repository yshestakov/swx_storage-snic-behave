Feature: SmartNIC is configured on the host

    Scenario: SmartNIC presents 2 HCAs as PCI devs
        Given arch is x86_64
        When execute `lspci -n -d 15b3:a2d2:0200`
        Then have 1 records

    Scenario: SmartNIC presents NVMe as PCI dev
        Given arch is x86_64
        When execute `lspci -n -d ::0108`
        Then have 1 record

    @slow
    Scenario: BF is in "SmartNIC" mode
        Given mst service is loaded
        When  query mlxconfig -d /dev/mst/mt41682_pciconf0
         Then have INTERNAL_CPU_MODEL EMBEDDED_CPU(1)

    Scenario: RSHIM network interface to SmartNIC
        Given rshim_net module is loaded
         When interface name is tmfifo_net0
         Then mac is 00:1a:ca:ff:ff:02
          And state is UP
          And driver is virtio_net

    Scenario: RSHIM network bridge
        Given has bridge tmfifo_br
         Then ipaddr is 192.168.100.1
          And mac is 00:1a:ca:ff:ff:02
          And state is UP
