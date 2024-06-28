﻿# -- coding: utf-8 --

import sys
from ctypes import *

sys.path.append("../MVSDK")
from IMVApi import *

MONO_CHANNEL_NUM=1
RGB_CHANNEL_NUM=3
BGR_CHANNEL_NUM=3

def displayDeviceInfo(deviceInfoList):  
    print("Idx  Type   Vendor              Model           S/N                 DeviceUserID    IP Address")
    print("------------------------------------------------------------------------------------------------")
    for i in range(0,deviceInfoList.nDevNum):
        pDeviceInfo=deviceInfoList.pDevInfo[i]
        strType=""
        strVendorName=""
        strModeName = ""
        strSerialNumber=""
        strCameraname=""
        strIpAdress=""
        for str in pDeviceInfo.vendorName:
            strVendorName = strVendorName + chr(str)
        for str in pDeviceInfo.modelName:
            strModeName = strModeName + chr(str)
        for str in pDeviceInfo.serialNumber:
            strSerialNumber = strSerialNumber + chr(str)
        for str in pDeviceInfo.cameraName:
            strCameraname = strCameraname + chr(str)
        for str in pDeviceInfo.DeviceSpecificInfo.gigeDeviceInfo.ipAddress:
                strIpAdress = strIpAdress + chr(str)
        if pDeviceInfo.nCameraType == typeGigeCamera:
            strType="Gige"
        elif pDeviceInfo.nCameraType == typeU3vCamera:
            strType="U3V"
        print ("[%d]  %s   %s    %s      %s     %s           %s" % (i+1, strType,strVendorName,strModeName,strSerialNumber,strCameraname,strIpAdress))

def selectImageFlipType():
    imageFlipTypeCnt=2
    print("--------------------------------------------")
    print("\t0.Image Vertical Flip")
    print("\t1.Image Horizontal Flip")
    print("--------------------------------------------")
    inputIndex = input("Please select the flip type index: ")

    if int(inputIndex) >=imageFlipTypeCnt|int(inputIndex)<0:
        print ("intput error!")
        return IMV_INVALID_PARAM

    return  int(inputIndex)
    
def imageFlip(cam,frame,imageFlipType):
    stPixelConvertParam=IMV_PixelConvertParam()
    stFlipImageParam=IMV_FlipImageParam()
    pConvertBuf=None
    nChannelNum=0
    
    memset(byref(stFlipImageParam),0,sizeof(stFlipImageParam))
    if IMV_EPixelType.gvspPixelMono8==frame.frameInfo.pixelFormat:
        stFlipImageParam.pSrcData = frame.pData
        stFlipImageParam.nSrcDataLen = frame.frameInfo.width * frame.frameInfo.height * MONO_CHANNEL_NUM
        stFlipImageParam.ePixelFormat = frame.frameInfo.pixelFormat
        nChannelNum = MONO_CHANNEL_NUM
    elif IMV_EPixelType.gvspPixelBGR8==frame.frameInfo.pixelFormat:
        stFlipImageParam.pSrcData = frame.pData
        stFlipImageParam.nSrcDataLen = frame.frameInfo.width * frame.frameInfo.height * BGR_CHANNEL_NUM
        stFlipImageParam.ePixelFormat = frame.frameInfo.pixelFormat
        nChannelNum = BGR_CHANNEL_NUM
    elif IMV_EPixelType.gvspPixelRGB8==frame.frameInfo.pixelFormat:
        stFlipImageParam.pSrcData = frame.pData
        stFlipImageParam.nSrcDataLen = frame.frameInfo.width * frame.frameInfo.height * RGB_CHANNEL_NUM
        stFlipImageParam.ePixelFormat = frame.frameInfo.pixelFormat
        nChannelNum = RGB_CHANNEL_NUM

    #MONO8/RGB24/BGR24以外的格式都转化成BGR24
    else:
        nConvertBufSize = frame.frameInfo.width * frame.frameInfo.height * BGR_CHANNEL_NUM;
        pConvertBuf=(c_ubyte * nConvertBufSize)()
        memset(byref(stPixelConvertParam), 0, sizeof(stPixelConvertParam))
        stPixelConvertParam.nWidth = frame.frameInfo.width
        stPixelConvertParam.nHeight = frame.frameInfo.height
        stPixelConvertParam.ePixelFormat = frame.frameInfo.pixelFormat
        stPixelConvertParam.pSrcData = frame.pData
        stPixelConvertParam.nSrcDataLen = frame.frameInfo.size
        stPixelConvertParam.nPaddingX = frame.frameInfo.paddingX
        stPixelConvertParam.nPaddingY = frame.frameInfo.paddingY
        stPixelConvertParam.eBayerDemosaic = IMV_EBayerDemosaic.demosaicNearestNeighbor
        stPixelConvertParam.eDstPixelFormat = IMV_EPixelType.gvspPixelBGR8
        stPixelConvertParam.pDstBuf = pConvertBuf
        stPixelConvertParam.nDstBufSize = nConvertBufSize

        nRet=cam.IMV_PixelConvert(stPixelConvertParam)
        if IMV_OK==nRet:
            stFlipImageParam.pSrcData = pConvertBuf
            stFlipImageParam.nSrcDataLen = stPixelConvertParam.nDstDataLen
            stFlipImageParam.ePixelFormat = IMV_EPixelType.gvspPixelBGR8
            nChannelNum = BGR_CHANNEL_NUM
        else:
            stFlipImageParam.pSrcData=None
            print("image convert to BGR8 failed! ErrorCode[%d]", nRet)
    bEnd=True
    while bEnd:
        if None==stFlipImageParam.pSrcData:
            print("stFlipImageParam pSrcData is NULL!")
            break
        nFlipBufSize=frame.frameInfo.width * frame.frameInfo.height * nChannelNum
        pFlipBuf=(c_ubyte*nFlipBufSize)()

        stFlipImageParam.nWidth = frame.frameInfo.width
        stFlipImageParam.nHeight = frame.frameInfo.height
        stFlipImageParam.eFlipType = imageFlipType
        stFlipImageParam.pDstBuf = pFlipBuf
        stFlipImageParam.nDstBufSize = nFlipBufSize

        nRet=cam.IMV_FlipImage(stFlipImageParam)

        if IMV_OK == nRet:
            if IMV_EFlipType.typeFlipVertical == imageFlipType:
                print("Image vertical flip successfully!")
                FileName="verticalFlip.bin"
                hFile=open(FileName.encode('ascii'), "wb")
            else:
                print("Image horizontal flip successfully!")
                FileName="horizontalFlip.bin"
                hFile=open(FileName.encode('ascii'), "wb")

            try:
                img_buff = (c_ubyte * stFlipImageParam.nDstBufSize)()
                cdll.msvcrt.memcpy(byref(img_buff), stFlipImageParam.pDstBuf, stFlipImageParam.nDstBufSize)
                hFile.write(img_buff)
            except:
                print("save file executed failed")
            finally:
                hFile.close() 

        else:
            if IMV_EFlipType.typeFlipVertical == imageFlipType:
                print("Image vertical flip failed! ErrorCode[%d]", nRet)
            else:
                print("Image horizontal flip failed! ErrorCode[%d]", nRet)
            if None!=pConvertBuf:
                del pConvertBuf
                pConvertBuf = None
            if None!=pFlipBuf:
                del pFlipBuf
        bEnd=False

if __name__ == "__main__":
    deviceList=IMV_DeviceList()
    interfaceType=IMV_EInterfaceType.interfaceTypeAll
    frame=IMV_Frame()
    # 枚举设备
    nRet=MvCamera.IMV_EnumDevices(deviceList,interfaceType)
    if IMV_OK != nRet:
        print("Enumeration devices failed! ErrorCode",nRet)
        sys.exit()
    if deviceList.nDevNum == 0:
        print ("find no device!")
        sys.exit()

    print("deviceList size is",deviceList.nDevNum)

    displayDeviceInfo(deviceList)

    nConnectionNum = input("Please input the camera index: ")

    if int(nConnectionNum) > deviceList.nDevNum:
        print ("intput error!")
        sys.exit()

    cam=MvCamera()
    # 创建设备句柄
    nRet=cam.IMV_CreateHandle(IMV_ECreateHandleMode.modeByIndex,byref(c_void_p(int(nConnectionNum)-1)))
    if IMV_OK != nRet:
        print("Create devHandle failed! ErrorCode",nRet)
        sys.exit()

    # 打开相机
    nRet=cam.IMV_Open()
    if IMV_OK != nRet:
        print("Open devHandle failed! ErrorCode",nRet)
        sys.exit()
      
    # 开始拉流
    nRet=cam.IMV_StartGrabbing()
    if IMV_OK != nRet:
        print("Start grabbing failed! ErrorCode",nRet)
        sys.exit()
    
    # 取一帧图像
    nRet=cam.IMV_GetFrame(frame,500)
    if IMV_OK!=nRet:
        print("Get frame failed!ErrorCode[%d]" % nRet)
        sys.exit()

    # 选择图像翻转方式
    imageFlipType=selectImageFlipType()

    print("BlockId (%d) pixelFormat (%d), Start image flip..." % (frame.frameInfo.blockId,frame.frameInfo.pixelFormat))

    # 图片转化
    imageFlip(cam,frame,imageFlipType)

    # 释放图像缓存
    nRet=cam.IMV_ReleaseFrame(frame)
    if IMV_OK!=nRet:
        print("Release frame failed!Errorcode[%d]" % nRet)
        sys.exit()

    # 停止拉流
    nRet=cam.IMV_StopGrabbing()
    if IMV_OK != nRet:
        print("Stop grabbing failed! ErrorCode",nRet)
        sys.exit()
    
    # 关闭相机
    nRet=cam.IMV_Close()
    if IMV_OK != nRet:
        print("Close camera failed! ErrorCode",nRet)
        sys.exit()
    
    # 销毁句柄
    if(cam.handle):
        nRet=cam.IMV_DestroyHandle()
    
    print("---Demo end---")