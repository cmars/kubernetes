#!/bin/bash -xe

HERE=$(cd $(dirname $0); pwd)
cd ${HERE}

export CHARM_DIR=${HERE}/builds

# Generate local bundle. `snap install j2`. Needs CHARM_DIR set.
j2 local-bundle.yaml.j2 > local-bundle.yaml

function waitfor_uvt_kvm {
	m=$1
	shift
	if [ -z "$m" ]; then
		echo "missing arg"
		exit 1
	fi
	for i in {1..20}; do
		sleep $i
		ssh -o "StrictHostKeyChecking no" ubuntu@$(uvt-kvm ip ${m}) "uptime" && break
	done
}

# Unconditionally create KVM instances for workers.
# Deploy into a new model every time.
# Use teardown-local.bash to clean up.

m1=kubs_m$(pwgen -An1)
m2=kubs_m$(pwgen -An1)

virsh dominfo ${m1} || uvt-kvm create ${m1} release=xenial arch=amd64 --disk 32 --memory 4096
virsh dominfo ${m2} || uvt-kvm create ${m2} release=xenial arch=amd64 --disk 32 --memory 4096
waitfor_uvt_kvm ${m1}

(juju controllers --format json | jq -r '.controllers|keys|.[]' | grep k8s) || juju bootstrap k8s lxd
juju switch k8s
juju add-model k8s-$(pwgen -An1)

juju add-machine ssh:$(uvt-kvm ip ${m1})
juju add-machine ssh:$(uvt-kvm ip ${m2})

# Download kubernetes if we don't have it yet.
if [ ! -f kubernetes.tar.gz ]; then
	wget https://github.com/kubernetes/kubernetes/releases/download/v1.4.0-beta.11/kubernetes.tar.gz
fi
if [[ ! -f kubernetes-master.tar.gz || ! -f kubernetes-master.tar.gz ]]; then
	repackage-kube-release.bash kubernetes.tar.gz
fi

# Deploy locally-built, manually placed kubernetes workers & master with resources.
# Place the workers on KVM in advance of the bundle to control placement.
juju deploy ${CHARM_DIR}/kubernetes-worker --to 0 --resource kubernetes=kubernetes-worker.tar.gz
juju add-unit kubernetes-worker --to 1

sleep 5

# Everything else can get autoplaced onto LXD in the bundle.
juju deploy local-bundle.yaml
