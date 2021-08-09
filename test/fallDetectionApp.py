import argparse
import cv2
import torch
import os
import time
import pickle5 as pickle                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
from test.utils import Resize

from test.fallDetectionModule import detectFall
from test.visualizeModule import vis_frame
from source.alphapose.utils.config import update_config


"""----------------------------- Demo options -----------------------------"""
parser = argparse.ArgumentParser(prog="Fall Detection App",description="This program reads video frames and predicts fall",
                                epilog="Enjoy the program")
parser.add_argument("--cfg",type=str,required=False,default="source/configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml",
                    help="Alphapose configure file name",)
parser.add_argument("--checkpoint",type=str,required=False,default="source/pretrained_models/fast_res50_256x192.pth",
                    help="checkpoint file name",)
parser.add_argument("--detector", dest="detector", help="detector name", default="yolo")
parser.add_argument("--vis", default=True, action="store_true", help="visualize image")
parser.add_argument("--showbox", default=True, action="store_true", help="visualize human bbox")
parser.add_argument("--profile", default=False, action="store_true", help="add speed profiling at screen output")
parser.add_argument("--min_box_area", type=int, default=0, help="min box area to filter out")
parser.add_argument("--gpus",type=str,dest="gpus",default="0",
    help="choose which cuda device to use by index and input comma to use multi gpus, e.g. 0,1,2,3. (input -1 for cpu only)")
parser.add_argument("--flip", default=False, action="store_true", help="enable flip testing")
parser.add_argument("-vis","--vis_fast", dest="vis_fast", help="use fast rendering", action="store_true", default=False)
parser.add_argument("--saveOut", type=str, default="outputs/MixFall/test4.avi", help="Save display to video file.")
parser.add_argument("-df","--dataFormat", type=str, default='h36m', help="Input Skeleton data format")
parser.add_argument("-c","--cam", dest="inputvideo", help="video-name", default="examples/demo/test/test3.mp4")
parser.add_argument("--transform", default=False, action="store_true", help="Do you want to transform the angle?056")
parser.add_argument("-tfile","--transform_file",dest="transfile",help="transformation-file",
                    default="examples/transformation_file/trans_Angle_F.pickle",)
parser.add_argument("-cls","--classifier", dest="classmodel", type=str, default="dstanet", 
                    help="choose classifer model, defualt dnn model")

args = parser.parse_args()
cfg = update_config(args.cfg)
args.gpus = [int(args.gpus[0])] if torch.cuda.device_count() >= 1 else [-1]
args.device = torch.device("cuda:" + str(args.gpus[0]) if args.gpus[0] >= 0 else "cpu")

def main(args,cfg):

    n_frames = 10
    pose2d_size = 34
    pose3d_size = None
    humanData = torch.zeros([n_frames, pose2d_size])
    #humanData2 = np.zeros([n_frames, pose2d_size])
    
    fps_time = 0
    frameIdx = 0
    framenumber = -1
    tagI2W = ["Fall", "Stand"]
    groundtruth = []
    prediction_result = []
    count = 0
    cam_source = args.inputvideo
    im_name = cam_source.split("/")[-1]
    if type(cam_source) is str and os.path.isfile(cam_source):
        # capture video file usign VideoCapture handler.
        cap = cv2.VideoCapture(cam_source)
        if cap.isOpened()==False:
            print("Error opening video stream or file")
        # get width and height of frame
        fwidth = int(cap.get(3))
        fheight = int(cap.get(4))
        opath= os.path.dirname(args.saveOut)
        if not os.path.exists(opath):
            os.makedirs(opath)
        writer = cv2.VideoWriter(args.saveOut,cv2.VideoWriter_fourcc('M','J','P','G'),20, (fwidth,fheight))
    
    fallModule = detectFall(args,cfg,n_frames,pose2d_size,pose3d_size)
    handle = open("examples/demo/test/labels/" + im_name.split(".")[0] + ".pickle", "rb")
    print('Hadle', handle)
    dictlabel = pickle.load(handle)

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            # convert frame to RGB and resize with aspect ratio
            frame = Resize(frame,492,600)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            framenumber = framenumber + 1
            framenumber_ = "{:05d}".format(framenumber)
            human2d,poseDict,human3d = fallModule.getPose(image,im_name,args.dataFormat)
            if poseDict is 'zero':
                continue
            if frameIdx != n_frames:
                if args.dataFormat=='alphapose':
                    humanData[frameIdx, :] = human2d
                else:
                    humanData[frameIdx, :] = torch.from_numpy(human2d)
                frameIdx += 1
            if frameIdx == n_frames:
                #print(frameIdx, humanData)
                index, confidence = fallModule.predictFall(humanData, format=args.dataFormat)
                action_name = tagI2W[index]
                
                if index==0 and confidence<0.9:
                    index= 1
                    action_name = tagI2W[index]
                elif index==1 and confidence<0.9:
                    index = 0
                    action_name = tagI2W[index]
            
                #print("Conf:{:0.2f},Predicted Label:{}".format(confidence, action_name))
                #print("Pred:{},Predicted Label:{}".format(index, action_name))
                frame = vis_frame(frame, poseDict, args) 
                # render predicted class names on video frames
                if action_name == "Fall":
                    frame = cv2.putText(
                        frame,
                        text="FALLING",
                        org=(450, 50),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(0, 0, 255),
                        thickness=2,
                    )

                elif action_name == "Stand":
                    frame = cv2.putText(
                        frame,
                        text="STANDING",
                        org=(450, 50),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(0,255, 0),
                        thickness=2,
                    )
                
                frame = cv2.putText(
                    frame,
                    text="FPS:%0.2f"%(1 / (time.time() - fps_time)),
                    org=(15, 50),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1,
                    color=(255, 0, 255),
                    thickness=2,
                )

                fps_time = time.time()
                humanData[: n_frames - 1] = humanData[1:n_frames]
                frameIdx = n_frames - 1
                #write video
                dim = (int(fwidth), int(fheight))
                frameNew = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
                writer.write(frameNew.astype('uint8'))
                # set opencv window attributes
                window_name = "FallDetection"
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                #w,h= 600,492
                cv2.resizeWindow(window_name, 600, 492)
                # Show Frame.
                cv2.imshow(window_name, frame)
                #write frame
                count = count + 1
                framecount_ = "{:05d}".format(count)
                path = args.saveOut.split('.')[0]
                if not os.path.exists(path):
                    os.makedirs(path)
                path = os.path.join(path, 'frame'+framecount_+'.png')
                cv2.imwrite(path, frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                """Find recall precision and f1 score"""
                try:
                    label = dictlabel[framenumber_]
                    if label=="Nofall":
                        label="Stand"
                    groundtruth.append(1 if label == "Stand" else 0)
                    prediction_result.append(1 if action_name == "Stand" else 0)
                    print("Predicted Label:",action_name)
                    print("Ground Label:",label)
                except:
                    pass
        else:
            print("Cap could not read the frame")
            break
    
    fallModule.getScores(groundtruth,prediction_result)
    # Clear resource.
    cap.release()
    writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(args,cfg)

    '''
    # set prediction type
    predType = "alpha2d"
    if predType == "alpha2d":
        predict2d(args, cfg)
    elif predType == "hmseq":
        predictSeq(args, cfg)
    elif predType == "2d":
        predict2dFrame(args, cfg)
    elif predType == "2d3d":
        predict2d3dFrame(args, cfg)
    '''