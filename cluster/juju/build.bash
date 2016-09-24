#!/bin/bash

set -ex

HERE=$(cd $(dirname $0);pwd)
export JUJU_REPOSITORY=${HERE}
export LAYER_PATH=${HERE}/layers
export INTERFACE_PATH=${HERE}/interfaces

CHARMS="$@"
if [ -z "$CHARMS" ]; then
	CHARMS="kubernetes-master kubernetes-worker guestbook-all-in-one kubeapi-load-balancer"
fi

pushd ${HERE}/layers
for i in ${CHARMS}; do
	(cd $i; charm build .)
done
popd
