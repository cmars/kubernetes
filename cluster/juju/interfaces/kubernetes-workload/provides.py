from charms.reactive import RelationBase, scopes, hook
from charmhelpers.core import hookenv


class KubernetesWorkloadProvides(RelationBase):
    scope = scopes.SERVICE

    @hook('{provides:workload}-relation-joined')
    def joined(self):
        self.set_state('{relation-name}.create')

    @hook('{provides:workload}-relation-changed')
    def changed(self):
        self.set_state('{relation-name}.updated')

    @hook('{provides:workload}-relation-departed')
    def depart(self):
        self.remove_state('{relation-name}.loaded')

    def service_status(self):
        return self.get_remote('service_status', {})

    def set_service(self, name=None, contents=None):
        relation_info = {
            'service_name': name,
            'service_file': contents,
        }
        self.set_remote(**relation_info)
