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

import devicedata
import egress_cpu_queue
import egress_rqe_queue
import egress_uc_queue
import egress_mc_queue
import egress_service_pool
import egress_port_service_pool
import egress_uc_queue_group
import ingress_port_priority_group
import ingress_port_service_pool
import ingress_service_pool
import congestion_drop_counters
import time
import unittest

class ReportTypes:
    Report, Trigger, Threshold, CongestionDropCounters = range(4)

class BSTParser():
    def __init__(self):
        self.__reportType = None
        self.__devicedata = None
        self.__ingress_port_priority_group = []
        self.__ingress_port_service_pool = []
        self.__ingress_service_pool = []
        self.__egress_cpu_queue = []
        self.__egress_mc_queue = []
        self.__egress_port_service_pool = []
        self.__egress_rqe_queue = []
        self.__egress_service_pool = []
        self.__egress_uc_queue = []
        self.__egress_uc_queue_group = []
        self.__congestion_top_drops = []
        self.__congestion_top_port_queue_drops = []
        self.__congestion_port_drops = []
        self.__congestion_port_queue_drops = []

        self.__handlers = {
            "device": self.handleDeviceRealm,
            "ingress-port-priority-group": self.handleIngressPortPriorityGroupRealm,
            "ingress-port-service-pool": self.handleIngressPortServicePoolRealm,
            "ingress-service-pool": self.handleIngressServicePoolRealm,
            "egress-cpu-queue": self.handleEgressCPUQueueRealm,
            "egress-mc-queue": self.handleEgressMcQueueRealm,
            "egress-port-service-pool": self.handleEgressPortServicePoolRealm,
            "egress-rqe-queue": self.handleEgressRQEQueueRealm,
            "egress-service-pool": self.handleEgressServicePoolRealm,
            "egress-uc-queue": self.handleEgressUcQueueRealm,
            "egress-uc-queue-group": self.handleEgressUcQueueGroupRealm,
            "top-drops": self.handleCongestionTopDrops,
            "top-port-queue-drops": self.handleCongestionTopPortQueueDrops,
            "port-drops": self.handleCongestionPortDrops,
            "port-queue-drops": self.handleCongestionPortQueueDrops
        }

    def getReportType(self):
        return self.__reportType

    def getASICId(self):
        return self.__asicId;

    def getTimestamp(self):
        return self.__timestamp;

    def __repr__(self):
        return "BST"

    def handleDeviceRealm(self, data):
        self.__devicedata = devicedata.DeviceData()
        self.__devicedata.parse(data)

    def getDeviceData(self):
        return self.__devicedata

    def handleIngressPortPriorityGroupRealm(self, data):
        for x in data:
            t = ingress_port_priority_group.IngressPortPriorityGroup()
            if "port" in x:
                port = x["port"]
            else:
                port = None
            t.parse(x["data"], port)
            self.__ingress_port_priority_group.append(t) 

    def getIngressPortPriorityGroup(self):
        return self.__ingress_port_priority_group

    def handleIngressPortServicePoolRealm(self, data):
        for x in data:
            t = ingress_port_service_pool.IngressPortServicePool()
            if "port" in x:
                port = x["port"]
            else:
                port = None
            t.parse(x["data"], port)
            self.__ingress_port_service_pool.append(t) 

    def getIngressPortServicePool(self):
        return self.__ingress_port_service_pool

    def handleIngressServicePoolRealm(self, data):
        t = ingress_service_pool.IngressServicePool()
        t.parse(data)
        self.__ingress_service_pool.append(t) 

    def getIngressServicePool(self):
        return self.__ingress_service_pool

    def handleEgressCPUQueueRealm(self, data):
        t = egress_cpu_queue.EgressCPUQueue()
        t.parse(data)
        self.__egress_cpu_queue.append(t) 

    def getEgressCPUQueue(self):
        return self.__egress_cpu_queue

    def handleEgressMcQueueRealm(self, data):
        t = egress_mc_queue.EgressMcQueue()
        t.parse(data)
        self.__egress_mc_queue.append(t) 

    def getEgressMcQueue(self):
        return self.__egress_mc_queue

    def handleEgressPortServicePoolRealm(self, data):
        for x in data:
            t = egress_port_service_pool.EgressPortServicePool()
            if "port" in x:
                port = x["port"]
            else:
                port = None
            t.parse(x["data"], port)
            self.__egress_port_service_pool.append(t) 

    def getEgressPortServicePool(self):
        return self.__egress_port_service_pool

    def handleEgressRQEQueueRealm(self, data):
        t = egress_rqe_queue.EgressRQEQueue()
        t.parse(data)
        self.__egress_rqe_queue.append(t) 

    def getEgressRQEQueue(self):
        return self.__egress_rqe_queue

    def handleEgressServicePoolRealm(self, data):
        t = egress_service_pool.EgressServicePool()
        t.parse(data)
        self.__egress_service_pool.append(t) 

    def getEgressServicePool(self):
        return self.__egress_service_pool

    def handleEgressUcQueueRealm(self, data):
        t = egress_uc_queue.EgressUcQueue()
        t.parse(data)
        self.__egress_uc_queue.append(t) 

    def getEgressUcQueue(self):
        return self.__egress_uc_queue

    def handleEgressUcQueueGroupRealm(self, data):
        t = egress_uc_queue_group.EgressUcQueueGroup()
        t.parse(data)
        self.__egress_uc_queue_group.append(t) 

    def getEgressUcQueueGroup(self):
        return self.__egress_uc_queue_group 

    def handleCongestionTopDrops(self, data):
        t = congestion_drop_counters.PortDrops("top-drops")
        t.parse(data)
        self.__congestion_top_drops.append(t) 

    def getCongestionTopDrops(self):
        return self.__congestion_top_drops 

    def handleCongestionTopPortQueueDrops(self, data):
        t = congestion_drop_counters.PortQueueDrops("top-port-queue-drops")
        t.parse(data)
        self.__congestion_top_port_queue_drops.append(t) 

    def getCongestionTopPortQueueDrops(self):
        return self.__congestion_top_port_queue_drops 

    def handleCongestionPortDrops(self, data):
        t = congestion_drop_counters.PortDrops("port-drops")
        t.parse(data)
        self.__congestion_port_drops.append(t) 

    def getCongestionPortDrops(self):
        return self.__congestion_port_drops 

    def handleCongestionPortQueueDrops(self, data):
        t = congestion_drop_counters.PortQueueDrops("port-queue-drops")
        t.parse(data)
        self.__congestion_port_queue_drops.append(t) 

    def getCongestionPortQueueDrops(self):
        return self.__congestion_port_queue_drops 

    def dispatchParser(self, report):
        ret = True
        if "realm" in report and report["realm"] in self.__handlers:
            try:
                self.__handlers[report["realm"]](report["data"])
            except:
                ret = False
        elif "report-type" in report and report["report-type"] in self.__handlers:
            try:
                self.__handlers[report["report-type"]](report["data"])
            except:
                ret = False
        else:
            ret = False
        return ret

    def process(self, data):
        ret = True
        if self.valid(data):
            if data["method"] == "get-bst-report":
                self.__reportType = ReportTypes.Report
            elif data["method"] == "trigger-report":
                self.__reportType = ReportTypes.Trigger
            elif data["method"] == "get-bst-thresholds":
                self.__reportType = ReportTypes.Threshold
            elif data["method"] == "get-bst-congestion-drop-counters":
                self.__reportType = ReportTypes.CongestionDropCounters
            else:
                ret = False 

            if ret:
                self.__asicId = data["asic-id"]
                x = data["time-stamp"].strip()
                try:
                    self.__timestamp = time.strptime(x, "%Y-%m-%d - %H:%M:%S")
                except:
                    ret = False
                if ret:
                    for x in data["report"]:
                        ret = self.dispatchParser(x)  
                        if ret == False:
                            break
        else:
            ret = False
        return ret

    def valid(self, data):
        ret = True
        keys  = ["jsonrpc", "method", 
                 "asic-id", "version",
                 "time-stamp", "report"]

        for x in keys:
            if not x in data:
                ret = False
                break

        if ret:
            if data["method"] != "get-bst-report" and \
               data["method"] != "trigger-report" and \
               data["method"] != "get-bst-thresholds" and \
               data["method"] != "get-bst-congestion-drop-counters":
                ret = False

        if ret:
            if not type(data["report"]) == list:
                ret = False
            elif len(data["report"]) == 0:
                ret = False

        return ret

class TestParser(unittest.TestCase):

    def setUp(self):
        self.bst_report = {
            "jsonrpc": "2.0",
            "method": "get-bst-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:15:04 ",
            "report": [
                {
                    "realm": "device",
                    "data": 46
                }, {
                    "realm": "ingress-port-priority-group",
                    "data": [{
                            "port": "2",
                            "data": [[5, 45500, 44450]]
                        }, {
                            "port": "3",
                            "data": [[6, 25500, 24450]]
                        }]
                }, {
                    "realm": "ingress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 324]]
                        }, {
                            "port": "3",
                            "data": [[6, 366]]
                        }]
                }, {
                    "realm": "ingress-service-pool",
                    "data": [[1, 3240], [2, 3660]]
                }, {
                    "realm": "egress-cpu-queue",
                    "data": [[3, 4566, 0]]
                }, {
                    "realm": "egress-mc-queue",
                    "data": [[1, "1", 34, 89], [2, "4", 1244, 0], [3, "5", 0, 3]]
                }, {
                    "realm": "egress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 0, 324, 0]]
                        }, {
                            "port": "3",
                            "data": [[6, 0, 366, 0]]
                        }]
                }, {
                    "realm": "egress-rqe-queue",
                    "data": [[2, 3333, 4444], [5, 25, 45]]
                }, {
                    "realm": "egress-service-pool",
                    "data": [[2, 0, 0, 3240], [3, 3660, 0, 0]]
                }, {
                    "realm": "egress-uc-queue",
                    "data": [[6, "0", 1111]]
                }, {
                    "realm": "egress-uc-queue-group",
                    "data": [[6, 2222]]
                }]
        }

        self.trigger = {
            "jsonrpc": "2.0",
            "method": "trigger-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2014-11-18 - 00:13:08 ",
            "realm": "ingress-port-priority-group",
            "counter": "um-share-buffer-count",
            "port": "2",
            "priority-group": "5",
            "report": [
                {
                    "realm": "device",
                    "data": 46
                }, {
                    "realm": "ingress-port-priority-group",

                    "data": [{
                            "port": "2",
                            "data": [[5, 45500, 44450]]
                        }, {
                            "port": "3",
                            "data": [[6, 25500, 24450]]
                        }]
                }, {
                    "realm": "ingress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 324]]
                        }, {
                            "port": "3",
                            "data": [[6, 366]]
                        }]
                }, {
                    "realm": "ingress-service-pool",
                    "data": [[1, 3240], [2, 3660]]
                }, {
                    "realm": "egress-cpu-queue",
                    "data": [[3, 4566, 0]]
                }, {
                    "realm": "egress-mc-queue",
                    "data": [[1, "1", 34, 89], [2, "4", 1244, 0], [3, "5", 0, 3]]
                }, {
                    "realm": "egress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 0, 324, 0]]
                        }, {
                            "port": "3",
                            "data": [[6, 0, 366, 0]]
                        }]
                }, {
                    "realm": "egress-rqe-queue",
                    "data": [[2, 3333, 4444], [5, 25, 45]]
                }, {
                    "realm": "egress-service-pool",
                    "data": [[2, 0, 0, 3240], [3, 3660, 0, 0]]
                }, {
                    "realm": "egress-uc-queue",
                    "data": [[6, "0", 1111]]
                }, {
                    "realm": "egress-uc-queue-group",
                    "data": [[6, 2222]]
                }]
        }

        self.thresholds = {
            "jsonrpc": "2.0",
            "method": "get-bst-thresholds",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2014-11-14 - 00:15:04 ",
            "report": [
                {
                    "realm": "device",
                    "data": 46
                }, {
                    "realm": "ingress-port-priority-group",
                    "data": [{
                            "port": "2",
                            "data": [[5, 45500, 44450]]
                        }, {
                            "port": "3",
                            "data": [[6, 25500, 24450]]
                        }]
                }, {
                    "realm": "ingress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 324]]
                        }, {
                            "port": "3",
                            "data": [[6, 366]]
                        }]
                }, {
                    "realm": "ingress-service-pool",
                    "data": [[1, 3240], [2, 3660]]
                }, {
                    "realm": "egress-cpu-queue",
                    "data": [[3, 4566, 0]]
                }, {
                    "realm": "egress-mc-queue",
                    "data": [[1, "1", 34, 89], [2, "4", 1244, 0], [3, "5", 0, 3]]
                }, {
                    "realm": "egress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 0, 324, 0]]
                        }, {
                            "port": "3",
                            "data": [[6, 0, 366, 0]]
                        }]
                }, {
                    "realm": "egress-rqe-queue",
                    "data": [[2, 3333, 4444], [5, 25, 45]]
                }, {
                    "realm": "egress-service-pool",
                    "data": [[2, 0, 0, 3240], [3, 3660, 0, 0]]
                }, {
                    "realm": "egress-uc-queue",
                    "data": [[6, "0", 1111]]
                }, {
                    "realm": "egress-uc-queue-group",
                    "data": [[6, 2222]]
                }]
        }


        self.bst_report_unknown_method = {
            "jsonrpc": "2.0",
            "method": "get-foo-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2016-02-15 - 00:15:04 ",
            "report": [
                {
                    "realm": "device",
                    "data": 46
                }, {
                    "realm": "ingress-port-priority-group",
                    "data": [{
                            "port": "2",
                            "data": [[5, 45500, 44450]]
                        }, {
                            "port": "3",
                            "data": [[6, 25500, 24450]]
                        }]
                }, {
                    "realm": "ingress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 324]]
                        }, {
                            "port": "3",
                            "data": [[6, 366]]
                        }]
                }, {
                    "realm": "ingress-service-pool",
                    "data": [[1, 3240], [2, 3660]]
                }, {
                    "realm": "egress-cpu-queue",
                    "data": [[3, 4566, 0]]
                }, {
                    "realm": "egress-mc-queue",
                    "data": [[1, "1", 34, 89], [2, "4", 1244, 0], [3, "5", 0, 3]]

                }, {
                    "realm": "egress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 0, 324, 0]]
                        }, {
                            "port": "3",
                            "data": [[6, 0, 366, 0]]
                        }]
                }, {
                    "realm": "egress-rqe-queue",
                    "data": [[2, 3333, 4444], [5, 25, 45]]
                }, {
                    "realm": "egress-service-pool",
                    "data": [[2, 0, 0, 3240], [3, 3660, 0, 0]]
                }, {
                    "realm": "egress-uc-queue",
                    "data": [[6, "0", 1111]]
                }, {
                    "realm": "egress-uc-queue-group",
                    "data": [[6, 2222]]
                }]
        }

        self.bst_report_unknown_realm = {
            "jsonrpc": "2.0",
            "method": "get-bst-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2016-02-15 - 00:15:04 ",
            "report": [
                {
                    "realm": "mustard",
                    "data": 46
                }]
        }

        self.bst_report_bad_timestamp = {
            "jsonrpc": "2.0",
            "method": "get-bst-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "xxxxxx ",
            "report": [
                {
                    "realm": "device",
                    "data": 46
                }, {
                    "realm": "ingress-port-priority-group",
                    "data": [{
                            "port": "2",
                            "data": [[5, 45500, 44450]]
                        }, {
                            "port": "3",
                            "data": [[6, 25500, 24450]]
                        }]
                }, {
                    "realm": "ingress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 324]]
                        }, {
                            "port": "3",
                            "data": [[6, 366]]
                        }]
                }, {
                    "realm": "ingress-service-pool",
                    "data": [[1, 3240], [2, 3660]]
                }, {
                    "realm": "egress-cpu-queue",
                    "data": [[3, 4566, 0]]
                }, {
                    "realm": "egress-mc-queue",
                    "data": [[1, "1", 34, 89], [2, "4", 1244, 0], [3, "5", 0, 3]]

                }, {
                    "realm": "egress-port-service-pool",
                    "data": [{
                            "port": "2",
                            "data": [[5, 0, 324, 0]]
                        }, {
                            "port": "3",
                            "data": [[6, 0, 366, 0]]
                        }]
                }, {
                    "realm": "egress-rqe-queue",
                    "data": [[2, 3333, 4444], [5, 25, 45]]
                }, {
                    "realm": "egress-service-pool",
                    "data": [[2, 0, 0, 3240], [3, 3660, 0, 0]]
                }, {
                    "realm": "egress-uc-queue",
                    "data": [[6, "0", 1111]]
                }, {
                    "realm": "egress-uc-queue-group",
                    "data": [[6, 2222]]
                }]
        }

        self.bst_report_report_dict = {
            "jsonrpc": "2.0",
            "method": "get-bst-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2016-02-15 - 00:15:04 ",
            "report": {}
        }

        self.bst_report_empty_report = {
            "jsonrpc": "2.0",
            "method": "get-bst-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2016-02-15 - 00:15:04 ",
            "report": []
        }


        self.bst_report_missing_report = {
            "jsonrpc": "2.0",
            "method": "get-bst-report",
            "asic-id": "20",
            "version": "1",
            "time-stamp": "2016-02-15 - 00:15:04 "
        }

        self._top_drops = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-drops",
                "data": [{
                    "port": "2",
                    "data": 8500
                    }, {
                    "port": "8",
                    "data": 7550
                    }, {
                    "port": "6",
                    "data": 6500
                    }, {
                    "port": "1",
                    "data": 5550
                    }, {
                    "port": "7",
                    "data": 4500
                    }, {
                    "port": "10",
                    "data": 3550
                    }, {
                    "port": "20",
                    "data": 2500
                    }, {
                    "port": "19",
                    "data": 1550
                    }]
            }],
            "id": 1
        }

        self._top_drops_bad_method = {
            "jsonrpc": "2.0",
            "method": "get-bst-runnynose-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-drops",
                "data": [{
                    "port": "2",
                    "data": 8500
                    }, {
                    "port": "8",
                    "data": 7550
                    }, {
                    "port": "6",
                    "data": 6500
                    }, {
                    "port": "1",
                    "data": 5550
                    }, {
                    "port": "7",
                    "data": 4500
                    }, {
                    "port": "10",
                    "data": 3550
                    }, {
                    "port": "20",
                    "data": 2500
                    }, {
                    "port": "19",
                    "data": 1550
                    }]
            }],
            "id": 1
        }

        self._top_drops_missing_report = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "id": 1
        }

        self._top_drops_unknown_report_type = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "drop-tops",
                "data": [{
                    "port": "2",
                    "data": 8500
                    }, {
                    "port": "8",
                    "data": 7550
                    }, {
                    "port": "6",
                    "data": 6500
                    }, {
                    "port": "1",
                    "data": 5550
                    }, {
                    "port": "7",
                    "data": 4500
                    }, {
                    "port": "10",
                    "data": 3550
                    }, {
                    "port": "20",
                    "data": 2500
                    }, {
                    "port": "19",
                    "data": 1550
                    }]
            }],
            "id": 1
        }

        self._top_drops_missing_data = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-drops"
            }],
            "id": 1
        }

        self._top_drops_empty_data = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-drops",
                "data": []
            }],
            "id": 1
        }

        self._top_drops_data_object = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-drops",
                "data": {
                    "port": "2",
                    "data": 8500
                }
            }],
            "id": 1
        }

        self._port_drops = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "port-drops",
                "data": [{
                    "port": "2",
                    "data": 8500
                    }, {
                    "port": "8",
                    "data": 7550
                    }, {
                    "port": "6",
                    "data": 6500
                    }, {
                    "port": "1",
                    "data": 5550
                    }, {
                    "port": "7",
                    "data": 4500
                    }, {
                    "port": "10",
                    "data": 3550
                    }, {
                    "port": "20",
                    "data": 2500
                    }, {
                    "port": "19",
                    "data": 1550
                    }]
            }],
            "id": 1
        }

        self._port_queue_drops_bad_method = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-plop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-port-queue-drops",
                "data": [
                    {
                        "port": "1",
                        "queue-type": "ucast",
                        "data": [[1,8500],[2,8400], [3,156000]]
                    }, {
                        "port": "1",
                        "queue-type": "mcast",
                        "data": [[1,600],[2,400], [3,1000]]
                    }, {
                        "port": "2",
                        "queue-type": "ucast",
                        "data": [[1,500],[2,800], [3,56000]]
                    }, {
                        "port": "2",
                        "queue-type": "mcast",
                        "data": [[1,2600],[2,3400], [3,21000]]
                    }]
            }],
            "id": 1
        }

        self._port_queue_drops_missing_report = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "id": 1
        }

        self._port_queue_drops_unknown_report_type = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "no-such-report-type",
                "data": [
                    {
                        "port": "1",
                        "queue-type": "ucast",
                        "data": [[1,8500],[2,8400], [3,156000]]
                    }, {
                        "port": "1",
                        "queue-type": "mcast",
                        "data": [[1,600],[2,400], [3,1000]]
                    }, {
                        "port": "2",
                        "queue-type": "ucast",
                        "data": [[1,500],[2,800], [3,56000]]
                    }, {
                        "port": "2",
                        "queue-type": "mcast",
                        "data": [[1,2600],[2,3400], [3,21000]]
                    }]
            }],
            "id": 1
        }

        self._port_queue_drops_missing_data = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-port-queue-drops"
            }],
            "id": 1
        }

        self._port_queue_drops_empty_data = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-port-queue-drops",
                "data": []
            }],
            "id": 1
        }

        self._port_queue_drops_data_object = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-port-queue-drops",
                "data": 
                    {
                        "port": "1",
                        "queue-type": "ucast",
                        "data": [[1,8500],[2,8400], [3,156000]]
                    }
            }],
            "id": 1
        }

        self._top_port_queue_drops = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "top-port-queue-drops",
                "data": [
                    {
                        "port": "1",
                        "queue-type": "ucast",
                        "data": [[1,8500],[2,8400], [3,156000]]
                    }, {
                        "port": "1",
                        "queue-type": "mcast",
                        "data": [[1,600],[2,400], [3,1000]]
                    }, {
                        "port": "2",
                        "queue-type": "ucast",
                        "data": [[1,500],[2,800], [3,56000]]
                    }, {
                        "port": "2",
                        "queue-type": "mcast",
                        "data": [[1,2600],[2,3400], [3,21000]]
                    }]
            }],
            "id": 1
        }

        self._port_queue_drops = {
            "jsonrpc": "2.0",
            "method": "get-bst-congestion-drop-counters",
            "asic-id": "1",
            "version": "3",
            "time-stamp": "2016-1-1 - 00:15:04 ",
            "report": [{
                "report-type": "port-queue-drops",
                "data": [
                    {
                        "port": "1",
                        "queue-type": "ucast",
                        "data": [[1,8500],[2,8400], [3,156000]]
                    }, {
                        "port": "1",
                        "queue-type": "mcast",
                        "data": [[1,600],[2,400], [3,1000]]
                    }, {
                        "port": "2",
                        "queue-type": "ucast",
                        "data": [[1,500],[2,800], [3,56000]]
                    }, {
                        "port": "2",
                        "queue-type": "mcast",
                        "data": [[1,2600],[2,3400], [3,21000]]
                    }]
            }],
            "id": 1
        }

    def test_unknown_method_bst(self):
        rep = BSTParser()
        ret = rep.process(self.bst_report_unknown_method)
        self.assertEqual(ret, False)

    def test_unknown_realm(self):
        rep = BSTParser()
        ret = rep.process(self.bst_report_unknown_realm)
        self.assertEqual(ret, False)

    def test_bad_timestamp(self):
        rep = BSTParser()
        ret = rep.process(self.bst_report_bad_timestamp)
        self.assertEqual(ret, False)

    def test_report_dict(self):
        rep = BSTParser()
        ret = rep.process(self.bst_report_report_dict)
        self.assertEqual(ret, False)

    def test_empty_report(self):
        rep = BSTParser()
        ret = rep.process(self.bst_report_empty_report)
        self.assertEqual(ret, False)

    def test_missing_report(self):
        rep = BSTParser()
        ret = rep.process(self.bst_report_missing_report)
        self.assertEqual(ret, False)

    def test_bst_report(self):
        rep = BSTParser()
        ret = rep.process(self.bst_report)
        self.assertEqual(ret, True)
        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.Report)

        val = rep.getDeviceData()
        self.assertEqual(val.getValue(), 46)

        val = rep.getIngressPortPriorityGroup()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPriorityGroup(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 45500)
        self.assertEqual(n.getUmHeadroomBufferCount(), 44450)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)
        

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)
        
        self.assertEqual(n.getPriorityGroup(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 25500)
        self.assertEqual(n.getUmHeadroomBufferCount(), 24450)
        self.assertEqual(n.getPort(), "3")

        val = rep.getIngressPortServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)


        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 324)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "3")
        self.assertEqual(n.getServicePool(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 366)

        val = rep.getIngressServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 1)
        self.assertEqual(n.getUmShareBufferCount(), 3240)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 2)
        self.assertEqual(n.getUmShareBufferCount(), 3660)

        val = rep.getEgressCPUQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getCPUBufferCount(), 4566)
        self.assertEqual(n.getCPUQueueEntries(), 0)

        val = rep.getEgressMcQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getMCBufferCount(), 34)
        self.assertEqual(n.getMCQueueEntries(), 89)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getMCBufferCount(), 1244)
        self.assertEqual(n.getMCQueueEntries(), 0)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getMCBufferCount(), 0)
        self.assertEqual(n.getMCQueueEntries(), 3)

        val = rep.getEgressPortServicePool()

        it = iter(val)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 324)
        self.assertEqual(n.getMCShareQueueEntries(), 0)
        self.assertEqual(n.getPort(), "2")


        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 366)
        self.assertEqual(n.getMCShareQueueEntries(), 0)
        self.assertEqual(n.getPort(), "3")

        val = rep.getEgressRQEQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getRQEBufferCount(), 3333)
        self.assertEqual(n.getRQEQueueEntries(), 4444)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 5)
        self.assertEqual(n.getRQEBufferCount(), 25)
        self.assertEqual(n.getRQEQueueEntries(), 45)

        val = rep.getEgressServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 2)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 0)
        self.assertEqual(n.getMCShareQueueEntries(), 3240)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 3)
        self.assertEqual(n.getUmShareBufferCount(), 3660)
        self.assertEqual(n.getMCShareBufferCount(), 0)
        self.assertEqual(n.getMCShareQueueEntries(), 0)

        val = rep.getEgressUcQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 6)
        self.assertEqual(n.getPort(), "0")
        self.assertEqual(n.getUcQueueBufferCount(), 1111)

        val = rep.getEgressUcQueueGroup()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueueGroup(), 6)
        self.assertEqual(n.getUcBufferCount(), 2222)

    def test_trigger(self):
        rep = BSTParser()
        ret = rep.process(self.trigger)
        self.assertEqual(ret, True)
        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.Trigger)

        val = rep.getDeviceData()
        self.assertEqual(val.getValue(), 46)

        val = rep.getIngressPortPriorityGroup()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPriorityGroup(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 45500)
        self.assertEqual(n.getUmHeadroomBufferCount(), 44450)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)
        
        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)
        
        self.assertEqual(n.getPriorityGroup(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 25500)
        self.assertEqual(n.getUmHeadroomBufferCount(), 24450)
        self.assertEqual(n.getPort(), "3")

        val = rep.getIngressPortServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 324)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 366)
        self.assertEqual(n.getPort(), "3")

        val = rep.getIngressServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 1)
        self.assertEqual(n.getUmShareBufferCount(), 3240)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 2)
        self.assertEqual(n.getUmShareBufferCount(), 3660)

        val = rep.getEgressCPUQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getCPUBufferCount(), 4566)
        self.assertEqual(n.getCPUQueueEntries(), 0)

        val = rep.getEgressMcQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getMCBufferCount(), 34)
        self.assertEqual(n.getMCQueueEntries(), 89)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getMCBufferCount(), 1244)
        self.assertEqual(n.getMCQueueEntries(), 0)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getMCBufferCount(), 0)
        self.assertEqual(n.getMCQueueEntries(), 3)

        val = rep.getEgressPortServicePool()

        it = iter(val)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 324)
        self.assertEqual(n.getMCShareQueueEntries(), 0)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 366)
        self.assertEqual(n.getMCShareQueueEntries(), 0)
        self.assertEqual(n.getPort(), "3")

        val = rep.getEgressRQEQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getRQEBufferCount(), 3333)
        self.assertEqual(n.getRQEQueueEntries(), 4444)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 5)
        self.assertEqual(n.getRQEBufferCount(), 25)
        self.assertEqual(n.getRQEQueueEntries(), 45)

        val = rep.getEgressServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 2)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 0)
        self.assertEqual(n.getMCShareQueueEntries(), 3240)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 3)
        self.assertEqual(n.getUmShareBufferCount(), 3660)
        self.assertEqual(n.getMCShareBufferCount(), 0)
        self.assertEqual(n.getMCShareQueueEntries(), 0)

        val = rep.getEgressUcQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 6)
        self.assertEqual(n.getPort(), "0")
        self.assertEqual(n.getUcQueueBufferCount(), 1111)

        val = rep.getEgressUcQueueGroup()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueueGroup(), 6)
        self.assertEqual(n.getUcBufferCount(), 2222)

    def test_thresholds(self):
        rep = BSTParser()
        ret = rep.process(self.thresholds)
        self.assertEqual(ret, True)
        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.Threshold)

        val = rep.getDeviceData()
        self.assertEqual(val.getValue(), 46)

        val = rep.getIngressPortPriorityGroup()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPriorityGroup(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 45500)
        self.assertEqual(n.getUmHeadroomBufferCount(), 44450)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)
        
        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)
        
        self.assertEqual(n.getPriorityGroup(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 25500)
        self.assertEqual(n.getUmHeadroomBufferCount(), 24450)
        self.assertEqual(n.getPort(), "3")

        val = rep.getIngressPortServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 324)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 366)
        self.assertEqual(n.getPort(), "3")

        val = rep.getIngressServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 1)
        self.assertEqual(n.getUmShareBufferCount(), 3240)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 2)
        self.assertEqual(n.getUmShareBufferCount(), 3660)

        val = rep.getEgressCPUQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getCPUBufferCount(), 4566)
        self.assertEqual(n.getCPUQueueEntries(), 0)

        val = rep.getEgressMcQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getMCBufferCount(), 34)
        self.assertEqual(n.getMCQueueEntries(), 89)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getMCBufferCount(), 1244)
        self.assertEqual(n.getMCQueueEntries(), 0)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getMCBufferCount(), 0)
        self.assertEqual(n.getMCQueueEntries(), 3)

        val = rep.getEgressPortServicePool()

        it = iter(val)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 5)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 324)
        self.assertEqual(n.getMCShareQueueEntries(), 0)
        self.assertEqual(n.getPort(), "2")

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 6)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 366)
        self.assertEqual(n.getMCShareQueueEntries(), 0)
        self.assertEqual(n.getPort(), "3")

        val = rep.getEgressRQEQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getRQEBufferCount(), 3333)
        self.assertEqual(n.getRQEQueueEntries(), 4444)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 5)
        self.assertEqual(n.getRQEBufferCount(), 25)
        self.assertEqual(n.getRQEQueueEntries(), 45)

        val = rep.getEgressServicePool()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 2)
        self.assertEqual(n.getUmShareBufferCount(), 0)
        self.assertEqual(n.getMCShareBufferCount(), 0)
        self.assertEqual(n.getMCShareQueueEntries(), 3240)

        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getServicePool(), 3)
        self.assertEqual(n.getUmShareBufferCount(), 3660)
        self.assertEqual(n.getMCShareBufferCount(), 0)
        self.assertEqual(n.getMCShareQueueEntries(), 0)

        val = rep.getEgressUcQueue()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueue(), 6)
        self.assertEqual(n.getPort(), "0")
        self.assertEqual(n.getUcQueueBufferCount(), 1111)

        val = rep.getEgressUcQueueGroup()

        it = iter(val)
        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        subit = iter(n)
        try:
            n = next(subit)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getQueueGroup(), 6)
        self.assertEqual(n.getUcBufferCount(), 2222)

    def test_topDropsBadMethod(self):
        rep = BSTParser()
        ret = rep.process(self._top_drops_bad_method)
        self.assertEqual(ret, False)

    def test_topDropsMissingReport(self):
        rep = BSTParser()
        ret = rep.process(self._top_drops_missing_report)
        self.assertEqual(ret, False)

    def test_topDropsUnknownReportType(self):
        rep = BSTParser()
        ret = rep.process(self._top_drops_unknown_report_type)
        self.assertEqual(ret, False)

    def test_topDropsMissingData(self):
        rep = BSTParser()
        ret = rep.process(self._top_drops_missing_data)
        self.assertEqual(ret, False)

    def test_topDropsEmptyData(self):
        rep = BSTParser()
        ret = rep.process(self._top_drops_empty_data)
        self.assertEqual(ret, True)

    def test_topDropsDataObject(self):
        rep = BSTParser()
        ret = rep.process(self._top_drops_data_object)
        self.assertEqual(ret, False)

    def test_topDrops(self):
        rep = BSTParser()
        ret = rep.process(self._top_drops)
        self.assertEqual(ret, True)
        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.CongestionDropCounters)

        it = iter(rep.getCongestionTopDrops()[0])

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getCount(), 8500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "8")
        self.assertEqual(n.getCount(), 7550)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "6")
        self.assertEqual(n.getCount(), 6500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getCount(), 5550)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "7")
        self.assertEqual(n.getCount(), 4500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "10")
        self.assertEqual(n.getCount(), 3550)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "20")
        self.assertEqual(n.getCount(), 2500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "19")
        self.assertEqual(n.getCount(), 1550)

    def test_portDrops(self):
        rep = BSTParser()
        ret = rep.process(self._port_drops)
        self.assertEqual(ret, True)
        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.CongestionDropCounters)

        it = iter(rep.getCongestionPortDrops()[0])

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getCount(), 8500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "8")
        self.assertEqual(n.getCount(), 7550)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "6")
        self.assertEqual(n.getCount(), 6500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getCount(), 5550)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "7")
        self.assertEqual(n.getCount(), 4500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "10")
        self.assertEqual(n.getCount(), 3550)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "20")
        self.assertEqual(n.getCount(), 2500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "19")
        self.assertEqual(n.getCount(), 1550)

    def test_portQueueDropsBadMethod(self):
        rep = BSTParser()
        ret = rep.process(self._port_queue_drops_bad_method)
        self.assertEqual(ret, False)

    def test_portQueueDropsMissingReport(self):
        rep = BSTParser()
        ret = rep.process(self._port_queue_drops_missing_report)
        self.assertEqual(ret, False)

    def test_portQueueDropsUnknownReportType(self):
        rep = BSTParser()
        ret = rep.process(self._port_queue_drops_unknown_report_type)
        self.assertEqual(ret, False)

    def test_portQueueDropsMissingData(self):
        rep = BSTParser()
        ret = rep.process(self._port_queue_drops_missing_data)
        self.assertEqual(ret, False)

    def test_portQueueDropsEmptyData(self):
        rep = BSTParser()
        ret = rep.process(self._port_queue_drops_empty_data)
        self.assertEqual(ret, True)

    def test_portQueueDropsDataObject(self):
        rep = BSTParser()
        ret = rep.process(self._port_queue_drops_data_object)
        self.assertEqual(ret, False)

    def test_topPortQueueDrops(self):
        rep = BSTParser()
        ret = rep.process(self._top_port_queue_drops)
        self.assertEqual(ret, True)
        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.CongestionDropCounters)

        it = iter(rep.getCongestionTopPortQueueDrops()[0])

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 8500)
        self.assertEqual(n.getQueue(), 1)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 8400)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 156000)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 600)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 400)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 1000)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 800)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 56000)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 2600)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 3400)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 21000)

    def test_portQueueDrops(self):
        rep = BSTParser()
        ret = rep.process(self._port_queue_drops)
        self.assertEqual(ret, True)
        val = rep.getReportType()
        self.assertEqual(val, ReportTypes.CongestionDropCounters)

        it = iter(rep.getCongestionPortQueueDrops()[0])

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 8500)
        self.assertEqual(n.getQueue(), 1)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 8400)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 156000)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 600)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 400)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "1")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 1000)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 500)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 800)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "ucast")
        self.assertEqual(n.getCount(), 56000)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 1)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 2600)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 2)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 3400)

        try:
            n = next(it)
        except:
            self.assertEqual(False, True)

        self.assertEqual(n.getPort(), "2")
        self.assertEqual(n.getQueue(), 3)
        self.assertEqual(n.getQueueType(), "mcast")
        self.assertEqual(n.getCount(), 21000)

if __name__ == "__main__":
    unittest.main()
