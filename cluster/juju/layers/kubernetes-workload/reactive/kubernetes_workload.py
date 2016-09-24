import os

from charmhelpers.core import hookenv
from charms.reactive import when, set_state, remove_state
from charms.reactive.helpers import data_changed

from charms.kubernetes.workload import service_name, node_port


# TODO: support pod/service changes on upgrade-charm
#@hook('upgrade-charm')...


@when('kubernetes-workload.create')
def workload_create(k):
    service_file = os.path.join(hookenv.charm_dir(), 'workload.yaml')
    with open(service_file, 'r') as f:
        contents = f.read()
        k.set_service(name=service_name(), contents=contents)
    remove_state('kubernetes-workload.create')


@when('kubernetes-workload.updated')
def workload_updated(k):
    status = k.service_status()
    if data_changed('kubernetes-workload.service.status', status):
        if node_port(status=status):
            set_state('kubernetes-workload.service.available')
    remove_state('kubernetes-workload.updated')
