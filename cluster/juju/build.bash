#!/bin/bash

set -xe

HERE=$(cd $(dirname $0); pwd)
export JUJU_REPOSITORY=${HERE}
export LAYER_PATH=${HERE}/layers
export INTERFACE_PATH=${HERE}/interfaces

(cd ${HERE}/layers/guestbook-all-in-one; charm build)
(cd ${HERE}/layers/kubernetes-master; charm build)

