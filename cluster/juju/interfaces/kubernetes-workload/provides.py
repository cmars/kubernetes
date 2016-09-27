import json

from charms.reactive import RelationBase, scopes, hook
from charmhelpers.core import hookenv


class KubernetesWorkloadProvides(RelationBase):
    scope = scopes.SERVICE

    @hook('{provides:kubernetes-workload}-relation-{joined,changed}')
    def changed(self):
        conv = self._maybe_conversation()
        if conv:
            self.set_state('{relation_name}.create')
        if conv and conv.get_remote('service_status'):
            self.set_state('{relation_name}.update')

    @hook('{provides:kubernetes-workload}-relation-{departed}')
    def departed(self):
        conv = self._maybe_conversation()
        if conv:
            self.set_state('{relation_name}.delete')

    def _maybe_conversation(self):
        conv = None
        try:
            conv = self.conversation()
        except:
            pass
        return conv

    def service_status(self):
        status_json = self.get_remote('service_status')
        if status_json:
            print(status_json)
            return json.loads(status_json)
        return {}

    def set_service(self, name=None, contents=None):
        relation_info = {
            'service_name': name,
            'service_file': contents,
        }
        self.set_remote(**relation_info)
