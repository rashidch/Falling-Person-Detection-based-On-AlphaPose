from easydict import EasyDict as edict

cfg3 = edict()
cfg3.MODEL = 'dnntiny3d'
cfg3.CHEKPT = 'checkpoints/dnntiny_3D_Jun_16_Yungtay_AugmentedEF/epoch_488_loss_0.002251.pth'
cfg3.tagI2W = ["Fall","Stand"] # 2
cfg3.tagW2I = {w:i for i,w in enumerate(cfg3.tagI2W)}