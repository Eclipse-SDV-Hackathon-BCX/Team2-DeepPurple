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


# pylint: disable=C0103, C0413, E1101
import asyncio
import json
import logging
import signal

from sdv.util.log import (  # type: ignore
    get_opentelemetry_log_factory,
    get_opentelemetry_log_format,
)
from sdv.vehicle_app import VehicleApp, subscribe_topic
from sdv_model import Vehicle, vehicle  # type: ignore

# Configure the VehicleApp logger with the necessary log config and level.
logging.setLogRecordFactory(get_opentelemetry_log_factory())
logging.basicConfig(format=get_opentelemetry_log_format())
logging.getLogger().setLevel("DEBUG")
logger = logging.getLogger(__name__)

SET_DRIVER_TOPIC = "deeppurple/setDriver"


class DeepPurpleApp(VehicleApp):
    """BCX2022 Hackathon"""

    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client

    async def on_start(self):
        logger.info("on_start")
        await self.Vehicle.Cabin.Seat.Row1.Pos1.Position.set(0)

    @subscribe_topic(SET_DRIVER_TOPIC)
    async def on_set_driver_received(self, data_str: str) -> None:
        # Use the logger with the preferred log level (e.g. debug, info, error, etc)
        logger.info(
            "topic: %s received with the data: %s",
            SET_DRIVER_TOPIC,
            data_str,
        )

        data = json.loads(data_str)

        response_topic = SET_DRIVER_TOPIC + "/response"
        response_data = {
            "requestId": data["requestId"],
            "driverId": data["driverId"],
            "status": 0,
        }
        await self.Vehicle.Cabin.Seat.Row1.Pos1.Position.set(
            int(data["preferredPosition"])
        )

        await self.publish_mqtt_event(response_topic, json.dumps(response_data))


async def main():

    logger.info("Starting DeepPurpleApp...")
    vehicle_app = DeepPurpleApp(vehicle)
    await vehicle_app.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
