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

# pylint: disable=C0321
import json

import pytest
from sdv.test.inttesthelper import IntTestHelper
from sdv.test.mqtt_util import MqttClient

SET_DRIVER_TOPIC = "deeppurple/setDriver"
SET_DRIVER_TOPIC_RESP = SET_DRIVER_TOPIC + "/response"

GET_SEAT_POSITION_TOPIC = "deeppurple/getSeatPosition"
GET_SEAT_POSITION_TOPIC_RESP = GET_SEAT_POSITION_TOPIC + "/response"


@pytest.mark.asyncio
async def test_set_driver():
    mqtt_client = MqttClient()
    inttesthelper = IntTestHelper()
    print(f"{mqtt_client} can be used when your app compiles succesfully!")
    print(f"{inttesthelper} can be used when your app compiles succesfully!")

    # response = await inttesthelper.set_uint16_datapoint(
    #     name="Vehicle.Cabin.Seat.Row1.Pos1.Position", value=0
    # )
    # assert len(response.errors) == 0

    response_str = mqtt_client.publish_and_wait_for_response(
        request_topic=SET_DRIVER_TOPIC,
        response_topic=SET_DRIVER_TOPIC_RESP,
        payload={
            "driverId": "DriverA",
            "requestId": 1,
            "preferredPosition": 42,
            "lightingProfile": 1,
        },
    )

    response = json.loads(response_str)
    print(f"Received response: {response}")

    assert response == {"driverId": "DriverA", "requestId": 1, "status": 0}
