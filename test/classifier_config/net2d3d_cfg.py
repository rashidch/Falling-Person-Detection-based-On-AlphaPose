from easydict import EasyDict as edict

cfg2 = edict()
cfg2.MODEL = 'net'
cfg2.CHEKPT = 'checkpoints/dnn2d3d_Jun_18/epoch_1919_loss_3.681156.pth'
cfg2.tagI2W = ["Fall","Stand"] # 2
cfg2.tagW2I = {w:i for i,w in enumerate(cfg2.tagI2W)}
