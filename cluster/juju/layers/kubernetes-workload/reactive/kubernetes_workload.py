import os

from charmhelpers.core import hookenv
from charmhelpers.core.unitdata import kv
from charms.reactive import when, set_state, remove_state
from charms.reactive.helpers import data_changed

from charms.kubernetes.workload import service_name, node_port


# TODO: support pod/service changes on upgrade-charm
#@hook('upgrade-charm')...


@when('workload.create')
def workload_create(k):
    try:
        for fn in ('workload.yaml', 'workload.json'):
            service_file = os.path.join(hookenv.charm_dir(), fn)
            if os.path.exists(service_file):
                with open(service_file, 'r') as f:
                    contents = f.read()
                    k.set_service(name=service_name(), contents=contents)
                    return
        # TODO(cmars): raise exception because at this point we don't have a
        # workload to create
    finally:
        remove_state('workload.create')


@when('workload.update')
def workload_update(k):
    try:
        status = k.service_status()
        db = kv()
        db.set('workload.service.status', status)
        if status:
            set_state('workload.service.available')
    finally:
        remove_state('workload.update')


@when('workload.delete')
def workload_delete(_):
    remove_state('workload.service.available')
    remove_state('workload.delete')
