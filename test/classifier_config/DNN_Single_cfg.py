from easydict import EasyDict as edict

cfg9 = edict()
cfg9.MODEL = 'DNN_Single'
cfg9.CHEKPT = 'model/act_dnnSingle_10/epoch_727.pth'
cfg9.tagI2W = ["Fall","Stand", "Tie"] # 3
cfg9.tagW2I = {w:i for i,w in enumerate(cfg9.tagI2W)}

# cfg.CHEKPT = 'model/act_dnnSingle_5/epoch_1000.pth'
# cfg.tagI2W = ["jump","run","sit","stand","walk"]