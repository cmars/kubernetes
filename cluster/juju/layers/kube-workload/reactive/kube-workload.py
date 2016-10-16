import os
import shutil
from subprocess import check_call, check_output

from charms.reactive import when, when_not, set_state, remove_state, hook, is_state

from charmhelpers.core import hookenv
from charmhelpers.fetch.archiveurl import ArchiveUrlFetchHandler


@hook('upgrade-charm')
def upgrade():
    remove_state('kube-workload.available')
    set_state('kube-workload.updated')


@when_not('kube-workload.available')
def install_kube_workload():
    try:
        kubectl = hookenv.resource_get('kubectl')
    except Exception:
        message = 'Error fetching the kubectl resource.'
        hookenv.log(message)
        hookenv.status_set('blocked', message)
        return

    if not kubectl:
        hookenv.log('Missing kubectl resource.')
        hookenv.status_set('blocked', 'Missing kubectl resource.')
        return

    shutil.copyfile(kubectl, '/usr/local/bin/kubectl')
    os.chmod('/usr/local/bin/kubectl', 0o755)


@when('kube-api-client.available', 'kube-workload.available')
@when_not('kube-workload.configured')
def configure_kubectl(kube):
    os.makedirs('/root/.kube', exist_ok=True)
    with open('/root/.kube/config', 'w') as f:
        f.write(kube.kubeconfig())
    set_state('kube-workload.configured')
    remove_state('kube-api-client.available')


@when('kube-api-client.available', 'kube-workload.configured')
def reconfigure_kubectl(_):
    remove_state('kube-workload.configured')


@when('kube-api-client.available', 'kube-workload.configured')
@when_not('kube-workload.created')
def create_workload(kube):
    wf = workload_file()
    if wf:
        check_call(['kubectl', 'create', '-f', wf], shell=True)
        set_state('kube-workload.created')


@when('kube-workload.available', 'kube-workload.created', 'kube-workload.updated')
def refresh_workload(kube):
    remove_state('kube-workload.updated')
    wf = workload_file()
    if wf:
        check_call(['kubectl', 'replace', '-f', wf], shell=True)
 

@hook('stop')
def delete_workload(kube):
    wf = workload_file()
    if wf and is_state('kube-workload.available') and is_state('kube-workload.created'):
        check_call(['kubectl', 'delete', '-f', wf], shell=True)


def workload_file():
    for tryname in ('workload.yaml', 'workload.json'):
        if os.path.exists(tryname):
            return tryname
    return None
