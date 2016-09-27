from charmhelpers.core.unitdata import kv
from charms import layer


def service_name():
    layer_info = layer.options('kubernetes-workload')
    return layer_info.get('service')


def node_port(status=None):
    if status is None:
        status = service_status()
    # TODO: match nodePort based on tags if multiple? map them by tag?
    for port in status.get('spec', {}).get('ports', []):
        # TODO(cmars): tagging for services with multiple ports?
        nodePort = port.get('nodePort')
        if nodePort:
            return nodePort
    return None


def service_status():
    db = kv()
    return db.get('workload.service.status', {})
