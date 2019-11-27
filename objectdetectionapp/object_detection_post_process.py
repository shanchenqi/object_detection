#! /usr/bin/env python
# coding=utf-8
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
import sys
import hiai
from hiaiapp.appgraph import *
from hiaiapp.presenteragent import *
from datatype import *
from datetime import *

# constants
# object label font
kobjectLabelFontSize = 0.7  # double
kobjectLabelFontWidth = 2  # int

# confidence range
kConfidenceMin = 0.0  # doulbe.
kConfidenceMax = 1.0
# need to deal results when index is 2
kDealResultIndex = 2
# each results size
kEachResultSize = 7
# attribute index
kAttributeIndex = 1
# score index
kScoreIndex = 2
# anchor_lt.x index
kAnchorLeftTopAxisIndexX = 3
# anchor_lt.y index
kAnchorLeftTopAxisIndexY = 4
# anchor_rb.x index
kAnchorRightBottomAxisIndexX = 5
# anchor_rb.y index
kAnchorRightBottomAxisIndexY = 6
# object attribute
kAttributeobjectLabelValue = 1.0  # float.
kAttributeobjectDeviation = 0.00001
# percent
kScorePercent = 100  # int32

# object label text prefix
kobjectLabelTextPrefix = 'object:'
kobjectLabelTextSuffix = '%'
def get_classes(classes_path):
    '''loads the classes'''
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names
classes = get_classes('./classes.txt')
class objectDetectPostConfig:
    def __init__(self):
        self.confidence = None     #The confidence of object detection
        self.presenterIp = None    #The presenter server ip
        self.presentPort = None    #The presenter server port
        self.channelName = None    #The presenter server channel, default is vedio

class objectDetectionPostProcess(AppEngine):
    def __init__(self, aiConfig):
        print("Create post process engine start...")
        self.config = objectDetectPostConfig()
        self.ParseConfig(aiConfig)
        self.channel = self.OpenChannel()
        if self.channel < 0:
            raise Exception("Open presenter channel failed")

        print("Create post process engine success")

    def ParseConfig(self, aiConfig):
        #Get config from graph.config
        for item in aiConfig._ai_config_item:
            if item._AIConfigItem__name == "Confidence":
                self.config.confidence = float(item._AIConfigItem__value)
            if item._AIConfigItem__name == "PresenterIp":
                self.config.presenterIp = item._AIConfigItem__value
            if item._AIConfigItem__name == "PresenterPort":
                self.config.presenterPort = int(item._AIConfigItem__value)
            if item._AIConfigItem__name == "ChannelName":
                self.config.channelName = item._AIConfigItem__value
    
    #Create link socket with presenter server
    def OpenChannel(self):
        openchannelparam = OpenChannelParam()
        openchannelparam.host_ip = self.config.presenterIp
        openchannelparam.port = self.config.presenterPort
        openchannelparam.channel_name = self.config.channelName
        openchannelparam.content_type = 1
        return OpenChannel(openchannelparam)
 
    def IsInvalidConfidence(self, confidence):
        return (confidence <= kConfidenceMin) or (confidence > kConfidenceMax)

    def IsInvalidResults(self, attr, score, point_lt, point_rb):
        #if abs(attr - kAttributeobjectLabelValue) > kAttributeobjectDeviation:
         #   print("true1")
          #  return True
        #object detection confidence too low
        if (score < self.config.confidence or self.IsInvalidConfidence(score)) :
        #    print("true object detection confidence too low")
            return True    
        #object rectangle in the image is invalid
        if (point_lt.x == point_rb.x) and (point_lt.y == point_rb.y):
         #   print("ace rectangle in the image is invalid")
            return True
        return False

    #When inference failed, we just send origin jpeg image to presenter server to display
    def HandleOriginalImage(self, inference_res):
        imgParam = inference_res.imageParamList[0]
        
        ret = SendImage(self.channel, imgParam.imageId, imgParam.imageData, [])
        if ret != HIAI_APP_OK:
            print("Send image failed, return ")
 
    #Parse the object detection confidence and object position in the image from inference result
    def HandleResults(self, inferenceData):

        jpegImageParam = inferenceData.imageParamList[0]
    #    print("...type(jpegImageParam)...",jpegImageParam)
        inferenceResult = inferenceData.outputData[0][0]
        widthWithScale = round(inferenceData.widthScale * jpegImageParam.imageData.width, 3)
        widthWithScale = widthWithScale /1280*1024

      #  print("jpegImageParam.imageData.width",jpegImageParam.imageData.width)
        heightWithScale = round(inferenceData.heightScale * jpegImageParam.imageData.height, 3)
       # heightWithScale = heightWithScale/720*576
     #   print("jpegImageParam.imageData.height",jpegImageParam.imageData.height)
       # print("inferenceResult,attr",inferenceResult[0][0][0][1])
       # print("inferenceResult,score",inferenceResult[0][0][0][2])
    
    #    print("inferenceResult,one_result.lt.x",inferenceResult[0][0][0][3])
    #    print("inferenceResult, one_result.lt.y",inferenceResult[0][0][0][4])
    #    print("inferenceResult,one_result.rb.x",inferenceResult[0][0][0][5])
    #    print("inferenceResult,one_result.rb.y",inferenceResult[0][0][0][6])
    
        detectionResults = []
        for i in range(0, inferenceResult.shape[0]):
            for j in range(0, inferenceResult.shape[1]):
                for k in range(0, inferenceResult.shape[2]):
                    
                    result = inferenceResult[i][j][k]
                    attr = result[kAttributeIndex] #1
                    score = result[kScoreIndex] #object detection confidence 2
                    
                    #Get the object position in the image
                    one_result = DetectionResult()
                    one_result.lt.x = result[kAnchorLeftTopAxisIndexX] * widthWithScale #3
                    one_result.lt.y = result[kAnchorLeftTopAxisIndexY] * heightWithScale #4
                    one_result.rb.x = result[kAnchorRightBottomAxisIndexX] * widthWithScale #5
                    one_result.rb.y = result[kAnchorRightBottomAxisIndexY] * heightWithScale #6
                    # one_result.contours=
                   # print("inferenceResult,attr",inferenceResult[0][0][0][1])
                  #  print("inferenceResult,score",inferenceResult[0][0][0][2])
                   # print("one_result.lt.x",one_result.lt.x)
                   # print("one_result.lt.y",one_result.lt.y)
                   # print("one_result.rb.x",one_result.rb.x)
                   # print("one_result.rb.y",one_result.rb.y)
                    
                    if self.IsInvalidResults(attr, score, one_result.lt, one_result.rb):
                        
                        continue
                    print("score=%f, lt.x=%d, lt.y=%d, rb.x=%d rb.y=%d",
                          score, one_result.lt.x, one_result.lt.y,one_result.rb.x, one_result.rb.y)

                    score_percent = score * kScorePercent
                    #Construct the object detection confidence string

                    one_result.result_text = classes[int(attr)] +str(":")+ str(score_percent) + kobjectLabelTextSuffix
                    detectionResults.append(one_result)
        #Send the object position, confidence string and image to presenter server
        ret = SendImage(self.channel, jpegImageParam.imageId, jpegImageParam.imageData, detectionResults)
        if ret != HIAI_APP_OK:
            print("Post process engine send image failed")

        return True
    #The post process engine Entry
    def Process(self, data):
        start = datetime.now()

        if data.outputData == None or data.outputData[0] == None or data.status == False:
            print("post engine handle original image.")
            ret = self.HandleOriginalImage(data)
        else:
            ret = self.HandleResults(data)


        end = datetime.now() - start
      #  print("Post process exhoust ", end.total_seconds())

        if GetExitFlag() == True:
            print("Camera engine exit for exit flag be set")
            sys.exit(0)

        return ret
