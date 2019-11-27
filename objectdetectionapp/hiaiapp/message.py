#! /usr/bin/env python
# -*- coding:utf-8 -*-
#   =======================================================================
#
# Copyright (C) 2018, Hisilicon Technologies Co., Ltd. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   1 Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#   2 Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   3 Neither the names of the copyright holders nor the names of the
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#   =======================================================================
#

import threading
from multiprocessing import Queue, Lock
import dataqueue
from hiaiapp import *

class MsgQueueUnit():
    def __init__(self, msgTypeNameList):
        self.mutex = Lock()
        self.msgTypeList = msgTypeNameList
        self.msgQueue = Queue()
        self.dataQueue = dataqueue.Queue()

class MsgServer():

    _instance_lock = threading.Lock()
    msgQueueList = []

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(MsgServer, "_instance"):
            with MsgServer._instance_lock:
                if not hasattr(MsgServer, "_instance"):
                    MsgServer._instance = object.__new__(cls)
        return MsgServer._instance

    def SubscribMsg(self, subscribMsgList):
        msgQUnit = MsgQueueUnit(subscribMsgList)
        self.msgQueueList.append(msgQUnit)
        return msgQUnit

    def GetEngineMsgQueue(self, engine):
        for msgQ in self.msgQueueList:
            if engine == msgQ.engine:
                return msgQ

        return None

    def SendMsg(self, msgTypeName, msgData):
        for unit in self.msgQueueList:
            for type in unit.msgTypeList:
                if type == msgTypeName:
                    unit.mutex.acquire()
                    unit.dataQueue.put(msgData)
                    unit.mutex.release()

                    unit.msgQueue.put(msgTypeName)
                    return HIAI_APP_OK
        print("Send msg %s failed", msgTypeName)
        return HIAI_APP_ERROR

msgCenter = MsgServer()

def SendData(msgTypeStr, msgData):
    return msgCenter.SendMsg(msgTypeStr, msgData)

