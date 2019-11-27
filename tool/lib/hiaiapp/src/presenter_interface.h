/**
 * ============================================================================
 *
 * Copyright (C) 2018, Hisilicon Technologies Co., Ltd. All Rights Reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *   1 Redistributions of source code must retain the above copyright notice,
 *     this list of conditions and the following disclaimer.
 *
 *   2 Redistributions in binary form must reproduce the above copyright notice,
 *     this list of conditions and the following disclaimer in the documentation
 *     and/or other materials provided with the distribution.
 *
 *   3 Neither the names of the copyright holders nor the names of the
 *   contributors may be used to endorse or promote products derived from this
 *   software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 * ============================================================================
 */

#ifndef ASCENDDK_PRESENTER_AGENT_PRESENTER_INTERobject_H_
#define ASCENDDK_PRESENTER_AGENT_PRESENTER_INTERobject_H_

#include "ascenddk/presenter/agent/channel.h"
#include "ascenddk/presenter/agent/errors.h"
#include "ascenddk/presenter/agent/presenter_types.h"
#include "ascenddk/presenter/agent/presenter_channel.h"
#include "image_pool.h"

extern "C" {
#define PRESENTER_OK = 0
#define PRESENTER_ERROR(errorCode) (-1 * (errorCode))


#define	ERROR_CODE_START  100
#define	ERROR_CODE_INVALID_IP  (ERROR_CODE_START + 0)
#define	ERROR_CODE_INVALID_PORT (ERROR_CODE_START + 1)
#define	ERROR_CODE_INVALID_CHANNEL_NAME (ERROR_CODE_START + 2)
#define	ERROR_CODE_CHANNEL_NOEXIST (ERROR_CODE_START + 3)


struct OpenChannelParamC 
{
    uint16_t port;
	uint16_t content_type;
	char* host_ip;
	char* channel_name;
};

typedef struct DetectionResultC {
	ascend::presenter::Point lt;   //The coordinate of left top point
	ascend::presenter::Point rb;   //The coordinate of the right bottom point
	char* result_text;  // object:xx%
}DetectionResultC;

typedef struct _ImageFrameMsg {
	int channel;
	ascend::presenter::ImageFrame frame;
	ImageData srcImage;
}ImageFrameMsg;

int SendImage(int channel, ImageData& image, struct DetectionResultC* detectionResults, uint32_t size);
int OpenChannelEx(const struct OpenChannelParamC& param);
ascend::presenter::Channel* GetChannel(int channelIdx);
bool IsInValidIp(const std::string& ip);
bool IsInValidPort(int32_t port);
bool IsInValidChannelName(const std::string& channel_name);
int SendImageToServer(ImageFrameMsg* msg);
}

#endif /* ASCENDDK_PRESENTER_AGENT_PRESENTER_CHANNEL_H_ */
