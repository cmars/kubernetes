from charms.reactive import when, when_not, set_state, remove_state

from charms.kubernetes.workload import node_port


@when('serving.available')
def inception_available(app):
    port = node_port()
    if port:
        app.configure(port)
        remove_state('serving.available')
