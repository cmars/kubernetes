from subprocess import check_call

from charmhelpers.core import hookenv
from charmhelpers.core.unitdata import kv
from charms.reactive import when, when_not, set_state, remove_state
from charms import layer

from charms.kubernetes.workload import node_port


@when_not('node-local.installed')
def install_kubernetes_node_local():
    layer_opts = layer.options('kubernetes-node-local')
    for image_file in layer_opts.get('image-files', []):
        load_image_file(image_file)
    for image_rc in layer_opts.get('image-resources', []):
        load_image_rc(image_rc)
    set_state('node-local.installed')


def load_image_file(fn):
    check_call(['docker', 'load', '-i', fn], shell=False)


def load_image_rc(rc):
    rcfile = hookenv.resource_get(rc)
    load_image_file(rcfile)


@when('workload.service.available')
def service_available():
    try:
        port = node_port()
        if port:
            hookenv.open_port(port)
    finally:
        remove_state('workload.service.available')
