#!/bin/bash

set -xe

HERE=$(cd $(dirname $0); pwd)
export JUJU_REPOSITORY=${HERE}
export LAYER_PATH=${HERE}/layers
export INTERFACE_PATH=${HERE}/interfaces

juju deploy ${HERE}/local.yaml
juju attach kubernetes-master kubernetes=${HERE}/kubernetes-master.tar.gz
juju attach guestbook kubectl=${HERE}/kubectl

