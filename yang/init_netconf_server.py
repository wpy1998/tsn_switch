import os

commands = [
    'sysrepoctl -i ietf-yang-types.yang',
    "sysrepoctl -i ietf-interfaces.yang",
    'sysrepoctl -i ieee802-types.yang',
    'sysrepoctl -i ieee802-dot1q-types.yang',
    'sysrepoctl -i iana-if-type.yang',
    'sysrepoctl -i ieee802-dot1q-sched.yang',
    'sysrepoctl -i ieee802-dot1q-bridge.yang',
    'sysrepoctl -i ieee802-dot1q-pb.yang',
    'sysrepoctl -i ieee802-dot1q-preemption.yang',
    'sysrepoctl -i ieee802-dot1q-sched-bridge.yang',
    'sysrepoctl -i ieee802-dot1q-preemption-bridge.yang'
]
def run_command(command):
    os.popen(command)

for command in commands:
    run_command(command)