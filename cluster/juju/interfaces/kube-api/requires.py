import json

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KubeAPIRequireer(RelationBase):
    scope = scopes.SERVICE

    @hook('{requires:kube-api}-relation-changed')
    def joined_or_changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.available')
        conv.set_state('{relation_name}.connected')

    @hook('{requires:kube-api}-relation-departed')
    def joined_or_changed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')

    def created(self, service_name):
        conv = self.conversation()
        conv.set_remote(service_name=service_name)

    def kubeconfig(self):
        conv = self.conversation()
        return conv.get_remote('kubeconfig')

    def status(self):
        conv = self.conversation()
        status_json = self.get_remote('status')
        if status_json:
            return json.loads(status_json)
        return None
