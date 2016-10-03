#!/bin/bash -xe

HERE=$(cd $(dirname $0); pwd)
cd ${HERE}

export CHARM_DIR=${HERE}/builds

# Generate local bundle. `snap install j2`. Needs CHARM_DIR set.
j2 local-bundle.yaml.j2 > local-bundle.yaml

(juju controllers --format json | jq -r '.controllers|keys|.[]' | grep k8s-gce) || juju bootstrap k8s-gce google
juju switch k8s-gce

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

juju deploy ${CHARM_DIR}/inception
juju add-relation inception:workload kubernetes-master:workload
juju add-relation inception:node-guest kubernetes-worker:node-host

#juju deploy ${CHARM_DIR}/pachyderm
#juju add-relation pachyderm:workload kubernetes-master:workload
#juju add-relation pachyderm:node-guest kubernetes-worker:node-host

