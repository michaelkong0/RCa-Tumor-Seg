#### holdout.md
Has locations of dataset on HPC - personal tracker

#### predictHoldout.py
Attempt to manually run predictions. Does not work well, use the CLI commands instead

nnUNetv2_predict
-i <input dir> NEEDS SAME NAMING FORMAT
-o <output dir> will output same name
-chk <checkpoint_name.pth>
-c <config>
-f <folds> default (0,1,2,3,4) - input as it would be formatted as a python tuple i.e., if only one fold use: (0,)
may need -m <model dir> for exporting model. Must still have the fold_0, fold_1, etc. datastructure