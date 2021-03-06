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

class RQEBufferCount():
    def __init__(self):
        self.value = None
        self.isPercent = False

    def getValue(self):
        return self.value

    def getIsPercent(self):
        return self.isPercent

    def __repr__(self):
        return "rqe-buffer-count"

    def parse(self, data):
        self.value = data[1]
        self.isPercent = False

