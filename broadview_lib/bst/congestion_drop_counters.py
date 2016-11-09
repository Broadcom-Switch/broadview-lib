# (C) Copyright Broadcom Corporation 2016
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class PortDropsEntry():
    def __init__(self):
        self._port = None
        self._count = 0

    def getPort(self):
        return self._port

    def getCount(self):
        return self._count

class PortDrops():
    def __init__(self, label):
        self.__table = []
        self.__label = label

    def __repr__(self):
        return self.__label

    def __iter__(self):
        self.__n = 0
        return self

    def next(self):
        if self.__n >= len(self.__table):
            raise StopIteration
        else:
            n = self.__n
            self.__n += 1
            return self.__table[n]

    def parse(self, data):
        for x in data:
            val = PortDropsEntry()
            val._port = x["port"]
            val._count = x["data"]
            self.__table.append(val)

class PortQueueDropsEntry():
    def __init__(self):
        self._port = None
        self._queue_type = None
        self._count = 0
        self._queue = 0

    def getPort(self):
        return self._port

    def getQueueType(self):
        return self._queue_type

    def getQueue(self):
        return self._queue

    def getCount(self):
        return self._count

class PortQueueDrops():
    def __init__(self, label):
        self.__table = []
        self.__label = label

    def __repr__(self):
        return self.__label

    def __iter__(self):
        self.__n = 0
        return self

    def next(self):
        if self.__n >= len(self.__table):
            raise StopIteration
        else:
            n = self.__n
            self.__n += 1
            return self.__table[n]

    def parse(self, data):
        for x in data:
            for y in x["data"]:
                val = PortQueueDropsEntry()
                val._port = x["port"]
                val._queue_type = x["queue-type"]
                val._queue = y[0]
                val._count = y[1]
                self.__table.append(val)
