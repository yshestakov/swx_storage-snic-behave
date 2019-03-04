from os import uname
import os.path
import subprocess
import re
from behave import given, when, then, use_step_matcher


@given('arch is {arch}')
def given_arch(context, arch):
    _u = uname()
    return _u[4] == arch


@when('execute `{command}`')
def when_exec_command(context, command):
    context.stdout_capture = subprocess.check_output(command, shell=True)

use_step_matcher("re")
@then(u'have (?P<n>\d+) record(?P<a>.*)')
def then_have_records(context, n, a):
    _o = context.stdout_capture.splitlines()
    cnt = len(_o)
    assert cnt == int(n)


use_step_matcher("parse")
@given('mst service is loaded')
def run_mst_service(context):
    _o = subprocess.check_output(['/etc/init.d/mst', 'status'],
                                 stderr=subprocess.STDOUT)
    if b'not loaded' in _o:
        subprocess.check_output(['/etc/init.d/mst', 'start'],
                                stderr=subprocess.STDOUT)

@when('query mlxconfig -d {device}')
def when_query_mlxconfig(context, device):
    cmd = ['/usr/bin/mlxconfig', '-d', device, 'q']
    context.mlxconfig = subprocess.check_output(cmd)

use_step_matcher("re")
@then('have (?P<keyword>\w+)[=\s](?P<value>\S+)')
def then_have_kv(context, keyword, value):
    found_it = False
    for line in context.mlxconfig.splitlines():
        m = re.search('(\w+)\s+(\S+)', str(line))
        if m is None:
            continue
        if m.group(1) == keyword:
            # print("Found '%s' = '%s' exp '%s'" % (keyword, m.group(2), value))
            assert m.group(2) == str(value), m.group(2)
            found_it = True
    # return False
    if not found_it:
        print("{{{%s}}}" % context.mlxconfig)
        raise AssertionError("Not found %s=%s" % (keyword, value))

use_step_matcher("parse")
def given_ipaddr(context, iface, ipaddr):
    cmd = ['/sbin/ip', 'a', 'l', iface]
    context.ip_iface = subprocess.check_output(cmd)


@given(u'{module} module is loaded')
def given_module_loaded(context, module):
    exp_mod = '%s ' % module
    with open('/proc/modules', 'r') as fi:
        for line in fi.readlines():
            if line.startswith(exp_mod):
                return True
    raise AssertionError(u'STEP: Given %s module is loaded' % module)


@when(u'interface name is {iface}')
def when_iface_name_is(context, iface):
    context.iface = iface
    assert os.path.exists(os.path.join('/sys/class/net', iface))
    cmd = ['/sbin/ip', 'a', 'l', iface]
    context.ip_iface = subprocess.check_output(cmd)
    """
9: tmfifo_net0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:1a:ca:ff:ff:02 brd ff:ff:ff:ff:ff:ff
    inet 192.168.100.1/24 brd 192.168.100.255 scope global tmfifo_net0
       valid_lft forever preferred_lft forever
    inet6 fe80::21a:caff:feff:ff02/64 scope link
       valid_lft forever preferred_lft forever
"""


@then(u'state is {state}')
def then_iface_state_is(context, state):
    # UP or DOWN
    m = re.search('state\s(\w+)', str(context.ip_iface))
    if m is None:
        raise AssertionError(u"STEP: no 'state is %s' found" % state)
    assert m.group(1) == str(state), m.group(1)

@then(u'ipaddr is {ipaddr}')
def then_iface_ipaar_is(context, ipaddr):
    m = re.search('net\s([\d.]+)/', str(context.ip_iface))
    if m is None:
        raise AssertionError(u"STEP: no 'inet %s' found" % ipaddr)
    assert m.group(1) == str(ipaddr), m.group(1)

@then(u'mac is {mac}')
def then_iface_mac_is(context, mac):
    m = re.search('link/ether\s([\d:a-f]+)', str(context.ip_iface))
    if m is None:
        raise AssertionError(u"STEP: no 'link/ether %s' found" % mac)
    assert m.group(1) == str(mac), m.group(1)


@then(u'driver is {driver}')
def then_driver_is(context, driver):
    cmd = ['ethtool', '-i', context.iface]
    _o = subprocess.check_output(cmd)
    m = re.search('driver:\s(\w+)', str(_o))
    if m is None:
        raise AssertionError("STEP: no 'driver is %s' found" % context.iface)
    assert m.group(1) == str(driver), m.group(1)

@given('has bridge {iface}')
def given_bridge(context, iface):
    context.iface = iface
    sys_fn = '/sys/class/net/%s/bridge' % iface
    assert os.path.exists(sys_fn)
    cmd = ['/sbin/ip', 'a', 'l', iface]
    context.ip_iface = subprocess.check_output(cmd)
