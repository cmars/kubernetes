import os
import tempfile

from charms.reactive import RelationBase, scopes, hook


class KubernetesWorkloadRequires(RelationBase):
    scope = scopes.SERVICE

    @hook('{requires:kubernetes-workload}-relation-{joined,changed}')
    def joined(self):
        conv = self._maybe_conversation()
        if conv and conv.get_remote('service_file'):
            conv.set_state('{relation_name}.load')

    @hook('{requires:kubernetes-workload}-relation-departed')
    def departed(self):
        conv = self._maybe_conversation()
        if conv and conv.get_remote('service_file'):
            conv.set_state('{relation_name}.unload')

    def _maybe_conversation(self):
        conv = None
        try:
            conv = self.conversation()
        except:
            pass
        return conv

    def service_name(self):
        return self.get_remote('service_name')

    def service_file(self):
        contents = self.get_remote('service_file')
        return self._temp_file(contents)

    def _temp_file(self, contents):
        tmpf = None
        try:
            tmpf = tempfile.NamedTemporaryFile(delete=False)
            with open(tmpf.name, 'w') as f:
                print(contents, file=f)
            return tmpf.name
        except Exception:
            if tmpf:
                os.unlink(tmpf.name)
            raise
 
    def status(self, service_status=None):
        relation_info = {
            'service_status': service_status,
        }
        self.set_remote(**relation_info)
