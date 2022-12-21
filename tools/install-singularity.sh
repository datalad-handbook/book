#!/bin/bash

set -e -u

release="$(curl -fsSL https://api.github.com/repos/sylabs/singularity/releases/latest | jq -r .tag_name)"
[ "${release}x" = "x" ] && echo "Failed to get latest singularity release name" && exit 1 || true
codename="$(lsb_release -cs)"
arch="$(dpkg --print-architecture)"
wget -O /tmp/singularity-ce.deb https://github.com/sylabs/singularity/releases/download/$release/singularity-ce_${release#v}-${codename}_$arch.deb
sudo dpkg -i /tmp/singularity-ce.deb
sudo apt-get install -f
