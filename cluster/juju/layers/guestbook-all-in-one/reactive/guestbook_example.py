from charms.reactive import when, when_not, set_state

from charms.kubernetes.workload import node_port


@when('website.available', 'workload.service.available')
def website_available(app):
    app.configure(node_port())
