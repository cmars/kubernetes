from charms.reactive import RelationBase, scopes, hook


class KubernetesWorkloadRequires(RelationBase):
    scope = scopes.SERVICE

    @hook('{requires:workload}-relation-joined')
    def joined(self):
        conv = self.conversation()
        if conv:
            conv.set_state('{relation-name}.load')

    @hook('{requires:workload}-relation-changed')
    def changed(self):
        conv = self.conversation()
        if conv:
            conv.set_state('{relation-name}.status')

    @hook('{requires:workload}-relation-departed')
    def departed(self):
        conv = self._maybe_conversation()
        if conv:
            conv.set_state('{relation-name}.unload')

    def _maybe_conversation(self):
        conv = None
        try:
            conv = self.conversation()
        except:
            pass
        return conv

    def service_name(self):
        conv = self.conversation()
        return conv.get_remote('service_name')

    def service_file(self, contents):
        conv = self.conversation()
        contents = self.get_remote('service_file')
        return self._temp_file(contents)

    def _temp_file(self, contents):
        tmpf = None
        try:
            tmpf = tempfile.NamedTemporaryFile(delete=False)
            with open(tmpf, 'wb') as f:
                f.write(contents)
            return tmpf
        except Exception:
            if tmpf:
                os.unlink(tmpf)
            raise
 
    def status(self, service_status=None):
        relation_info = {
            'service_status': service_status,
        }
        self.set_remote(**relation_info)
