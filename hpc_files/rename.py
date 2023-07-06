import glob
import SimpleITK as sitk

import os

import glob
import SimpleITK as sitk
import numpy as np
from scipy import ndimage
import pandas as pd 
import shutil
import xlsxwriter

def center(arr):
    out = []
    arr[arr!=-1] = 1
    for dim in ndimage.center_of_mass(arr):
        out.append(round(dim))
    return out

def get_bounding_box(x):
    """ Calculates the bounding box of a ndarray"""
    mask = x == 0
    bbox = []
    all_axis = np.arange(x.ndim)
    for kdim in all_axis:
        nk_dim = np.delete(all_axis, kdim)
        mask_i = mask.all(axis=tuple(nk_dim))
        dmask_i = np.diff(mask_i)
        idx_i = np.nonzero(dmask_i)[0]
        if(len(idx_i)==0):
            bbox.append(slice(100,110))
            continue
        low = min( idx_i )
        high = max( idx_i )
        s = slice(low + 1, high + 1)
        bbox.append(s)
    return bbox

def findCropBox(cen:tuple, img: tuple, crop:tuple):
    box = []
    for k in range(0,len(crop)):
        exp = round((crop[k]-1)/2) # the distance in any one direction, again assumes odd size
        if ((exp+cen[k]) < img[k]) and (cen[k] - exp >= 0): #both directions within the inner bound -- perfect, move on
            box.append(slice(cen[k] - exp,exp+cen[k]+1)) #center the slice on the center
        else:
            #THE CROP TO SIZE SHOULD NOT EXCEED THE IMG SIZE, SO THIS SHOULDN'T BE AN ISSUE IN BOTH DIRECTIONS
            if not ((exp+cen[k]) < img[k]): #the outer boundary is expanded past
                box.append(slice(img[k]-crop[k],img[k])) #push directly against the edge of the image
            else: # went below 0
                box.append(slice(0,crop[k]))
    if(len(crop)<3):
        box.append(slice(0,img[2]))
    return tuple(box)

def Reverse(tuples): ##needed because the simple ITK getarrayfromimage gives as z,y,x  - I am currently treating as x,y,z beacuse sitk images are xyz listed
    new_tup = tuples[::-1]
    return new_tup


#assumes that all of the dimensions in size are ODD
#should work for cropping in 2D (i.e., ignoring depth) and with 3D
def cropAll(size: tuple, img_dir: str, lbl_dir: str, xlsxfile: str, s_name:str="output"):
    imgs = glob.glob(img_dir+"/*.mha")
    imgs.sort()
    masks = glob.glob(lbl_dir+"/*.mha")
    masks.sort()
    assert len(imgs) == len(masks)

    r = sitk.ImageFileReader()
    w = sitk.ImageFileWriter()

    toExcel = [[],[]]

    for i in range(0,len(masks)):
        print(masks[i])
        r.SetFileName(masks[i])
        img = r.Execute()
        a = sitk.GetArrayFromImage(img)
        bbx = get_bounding_box(a)
        if bbx == "no":
            print("this file has an issue")
            continue
        arr = a[bbx[0].start:bbx[0].stop,bbx[1].start:bbx[1].stop,bbx[2].start:bbx[2].stop]
        c = center(arr)
        for j in range(0,len(c)):
            c[j] += bbx[j].start
        print(c)
        print(a.shape)
        cbox = findCropBox(Reverse(tuple(c)),Reverse(a.shape),size)
        cropped = img[cbox[0],cbox[1],cbox[2]]
        w.SetFileName(masks[i])
        w.Execute(cropped)


        w.SetFileName(imgs[i])
        r.SetFileName(imgs[i])
        w.Execute(r.Execute()[cbox[0],cbox[1],cbox[2]])

        toExcel[0].append(masks[i])
        toExcel[1].append(str(cbox))
    writer = pd.ExcelWriter(xlsxfile, engine='xlsxwriter')
    df = pd.DataFrame(toExcel).T
    df.to_excel(writer,sheet_name=s_name,index=False)
    writer.close()

def renameFile(file: str, dir: str, label: bool):

    c = file
    s = ""

    if "CCF" in file:
        s = "CCF"
    elif "UH" in file:
        s = "UH"
    elif "VA" in file:
        s = "VA"
    else:
        s = "UH"
    
    s = s + "_"
    for char in c:
        if char.isdigit():
            s = s+char
    if(s[-4:] == "0000"):
        s = s[:-4]
    
    if not label:
        s  = s + "_0000.mha"
    else:
        s = s + ".mha"
   
    os.rename(dir+"/"+file,dir+"/"+s)



def copyToDirs(source: str):
    images=r"/scratch/pbsjobs/job.282949.hpc/images"
    labels = r"/scratch/pbsjobs/job.282949.hpc/labels"
    
    files = glob.glob(dir+"/*.mha")
    label = ""
    img = ""
    if "label" in files[0] or "ask" in files[0] or "egment" in files[0]:
        label = files[0]
        img = files[1]
    else:
        label = files[1]
        img = files[0]
    
    shutil.copy2(label, labels)
    shutil.copy2(img, images)


def filterImage(img: str, val):
    r = sitk.ImageFileReader()
    r.SetFileName(img)
    a = r.Execute()
    arr = sitk.GetArrayFromImage(a)
    arr[arr != val] = 0
    changed = sitk.GetImageFromArray(arr)
    if not 1 in arr:
        print("ERROR WITH: " + img)
        print("NO TUMOR FOUND")
    w = sitk.ImageFileWriter()
    w.SetFileName(img)
    changed.CopyInformation(a)
    w.Execute(changed)

for dir in glob.glob(r"/scratch/pbsjobs/job.282949.hpc/raw/UH_preCRT/UH/*"):
    copyToDirs(dir)
for dir in glob.glob(r"/scratch/pbsjobs/job.282949.hpc/raw/VA_preCRT/*"):
    copyToDirs(dir)

for file in glob.glob(r"/scratch/pbsjobs/job.282949.hpc/labels/*.mha"):
    filterImage(file,1)
    renameFile(file.replace("/scratch/pbsjobs/job.282949.hpc/labels/",""),"/scratch/pbsjobs/job.282949.hpc/labels", True)

for file in glob.glob(r"/scratch/pbsjobs/job.282949.hpc/images/*.mha"):
    renameFile(file.replace("/scratch/pbsjobs/job.282949.hpc/images/",""),"/scratch/pbsjobs/job.282949.hpc/images", False)

cropAll(tuple([145,135]),r"/scratch/pbsjobs/job.282949.hpc/images",r"/scratch/pbsjobs/job.282949.hpc/labels",r"/mnt/pan/Data7/mfk58/coronalv3crop.xlsx")



