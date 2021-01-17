import os
import shutil
import json
import pandas as pd
import numpy as np
from loguru import logger

execResjson = "find -type f -iname 'alphapose-results_without_flip.json' "

alphaI2W = [ "nose","LEye","REye","LEar","REar","LShoulder","RShoulder", "LElbow","RElbow",\
"LWrist", "RWrist","LHip","RHip", "LKnee","Rknee", "LAnkle","RAnkle"]# neck is addtion

@logger.catch
def cleanJson(jslist:list):
    print('in clean')
    # jsitem = jslist[0]
    dicts =[]
    for jsitem in jslist:
        #print('len of keypoints list', len(jsitem['keypoints']))
        itKeypoints = np.array(jsitem['keypoints']).reshape(-1,3)
        print('keypoints:',itKeypoints.shape)
        idx = jsitem['idx']
        imgid= jsitem['image_id']
        box = jsitem['box']
        score = jsitem['score']
        pose_class = jsitem['pose_class'].split('_')[0]
        if(len(idx)>1):
            # logger.debug('muti-idx: %s | %s'%(imgid,idx.__str__()))
            idx = idx[0][0]
        else:
            idx= idx[0]
        d={'image_id': imgid, 'idx':idx, 'pos_class':pose_class, 'box':box, 'score':score}
        for i,xys in enumerate(itKeypoints):
            d[alphaI2W[i]+'_x'] = xys[0]
            d[alphaI2W[i]+'_y'] = xys[1]
        dicts.append(d)
    return dicts

def getParDirFromPath(path):
    p = os.path.split(path)[0]
    return os.path.split(p)[1]

@logger.catch    
def Jsons2Csv(filelist:list):
    for fpath in filelist:
        if(os.path.splitext(fpath)[1] != '.json'):
            logger.info('{} isn\'t json,skip',fpath)
            continue
        with open(fpath,'r') as f:
            jslist = json.load(f)
            df = pd.DataFrame(cleanJson(jslist))
            if(df['image_id'].duplicated().sum()>0):
                mode = df['idx'].mode().item()
                df = df.loc[df['idx'] == mode]
            _fpath =os.path.join(outpath,'%s.csv'%getParDirFromPath(fpath)) 
            df.to_csv(_fpath)
            logger.info('%d rows to %s'%(df.shape[0],_fpath))
            # os.remove(fpath)
            
if __name__ == "__main__":
    logger.add('train/data_pre/json2csv_{time}.log') 
    outpath = 'train/data'
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    with os.popen(execResjson) as p:
        jsonlist = p.read().splitlines()
        print(jsonlist)
        Jsons2Csv(jsonlist)

    



