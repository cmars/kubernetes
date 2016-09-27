#!/bin/bash -xe

HERE=$(cd $(dirname $0); pwd)
cd ${HERE}

export CHARM_DIR=${HERE}/builds

# Generate local bundle. `snap install j2`. Needs CHARM_DIR set.
j2 local-bundle.yaml.j2 > local-bundle.yaml

(juju controllers --format json | jq -r '.controllers|keys|.[]' | grep k8s) || juju bootstrap k8s canonistack/lcy02
juju switch k8s

# Download kubernetes if we don't have it yet.
if [ ! -f kubernetes.tar.gz ]; then
	wget https://github.com/kubernetes/kubernetes/releases/download/v1.4.0-beta.11/kubernetes.tar.gz
fi
if [[ ! -f kubernetes-master.tar.gz || ! -f kubernetes-master.tar.gz ]]; then
	repackage-kube-release.bash kubernetes.tar.gz
fi

juju deploy local-bundle.yaml
juju attach kubernetes-master kubernetes=kubernetes-master.tar.gz
juju attach kubernetes-worker kubernetes=kubernetes-worker.tar.gz

juju deploy ${CHARM_DIR}/guestbook
juju add-relation guestbook:workload kubernetes-master:workload
juju add-relation guestbook:node-guest kubernetes-worker:node-host

