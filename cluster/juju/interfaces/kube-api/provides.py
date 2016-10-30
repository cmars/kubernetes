from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KubeAPIProvider(RelationBase):
    scope = scopes.SERVICE

    @hook('{provides:kube-api}-relation-changed')
    def joined_or_changed(self):
        conv = self.conversation()
        if conv.get_remote('service_name'):
            conv.set_state('{relation_name}.wants-status')
        conv.set_state('{relation_name}.connected')

    @hook('{provides:kube-api}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')

    def kubeconfig(self, kubecfg):
        conv = self.conversation()
        conv.set_remote(kubeconfig=kubecfg, scope=scopes.GLOBAL)
        return True

    def service_name(self):
        conv = self.conversation()
        return conv.get_remote('service_name')

    def status(self, status):
        conv = self.conversation()
        conv.set_remote(status=status)
        return True
