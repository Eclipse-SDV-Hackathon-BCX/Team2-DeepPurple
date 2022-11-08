#!/bin/bash
# Copyright (c) 2022 Robert Bosch GmbH and Microsoft Corporation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

echo "#######################################################"
echo "### Running Databroker                              ###"
echo "#######################################################"

ROOT_DIRECTORY=$( realpath "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )/../../../.." )

# Get Data from AppManifest.json and save to ENV
UTILS_DIRECTORY="$ROOT_DIRECTORY/.vscode/scripts/runtime/utils"
source $UTILS_DIRECTORY/get-appmanifest-data.sh

NODERED_PORT='1880'
#export DATABROKER_GRPC_PORT='52001'
#export RUST_LOG="info,databroker=debug,vehicle_data_broker=debug"

RUNNING_CONTAINER=$(docker ps | grep "$NODERED_IMAGE" | awk '{ print $1 }')

if [ -n "$RUNNING_CONTAINER" ];
then
    docker container stop $RUNNING_CONTAINER
fi

docker run \
    -v $UTILS_DIRECTORY/nodered:/data \
    -p $NODERED_PORT:$NODERED_PORT \
    --network host \
    $NODERED_IMAGE:$NODERED_TAG
