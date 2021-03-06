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

import umsharebuffercount
import mcsharebuffercount
import mcsharequeueentries

class EgressServicePoolEntry():
    def __init__(self):
        self.__servicePool = None
        self._umsharebuffercount = umsharebuffercount.UmShareBufferCount()
        self._mcsharebuffercount = mcsharebuffercount.McShareBufferCount()
        self._mcsharequeueentries = mcsharequeueentries.McShareQueueEntries()

    def getServicePool(self):
        return self._servicePool

    def getUmShareBufferCount(self):
        return self._umsharebuffercount.value 

    def getMCShareBufferCount(self):
        return self._mcsharebuffercount.value

    def getMCShareQueueEntries(self):
        return self._mcsharequeueentries.value

class EgressServicePool():
    def __init__(self):
        self.__table = []

    def __repr__(self):
        return "egress-service-pool"

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
            val = EgressServicePoolEntry()
            val._servicePool = x[0]
            val._umsharebuffercount.parse(x)
            val._mcsharebuffercount.parse(x)
            val._mcsharequeueentries.parse(x)
            self.__table.append(val)



