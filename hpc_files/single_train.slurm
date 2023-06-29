#!/bin/bash
#SBATCH -p gpu
#SBATCH -C gpu2v100
#SBATCH -N 1 
#SBATCH -n 10
#SBATCH --gres=gpu:1
#SBATCH --mem=50gb
#SBATCH -t 40:00:00

export HOME=/mnt/pan/Data7/mfk58
cd /mnt/pan/Data7/mfk58
module purge
module load CUDA/11.7.0
module load cuDNN/8.4.1.50-CUDA-11.7.0
module load Python/3.10.4-GCCcore-11.3.0
module load PyTorch/1.12.1-foss-2022a-CUDA-11.7.0  
python --version
python -m venv nnunetGPU
source ~/nnunetGPU/bin/activate
pip3 install torch torchvision torchaudio
python -c "import torch;assert torch.cuda.is_available()"
pip3 install nnunetv2
export nnUNet_raw=/scratch/pbsjobs/job.278992.hpc/nnUNet_raw
export nnUNet_preprocessed=/mnt/pan/Data7/mfk58/nnUNet_preprocessed
export nnUNet_results=/mnt/pan/Data7/mfk58/nnUNet_results

CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 167 3d_fullres 0 --npz --c 