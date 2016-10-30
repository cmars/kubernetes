from charms.reactive import when, when_not, set_state, remove_state

from charms.kubernetes import node_port


@when('website.available')
def website_available(app):
    port = node_port()
    if port:
        app.configure(port)
        remove_state('website.available')
