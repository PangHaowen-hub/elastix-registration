import pyelastix
import os
from tqdm import trange
import SimpleITK as sitk
import numpy as np
import shutil


def get_listdir(path):
    tmp_list = []
    for file in os.listdir(path):
        if os.path.splitext(file)[1] == '.gz':
            file_path = os.path.join(path, file)
            tmp_list.append(file_path)
    return tmp_list


if __name__ == '__main__':
    f_img_list = get_listdir(r'H:\PRM\image_580_nii\i_lung')
    f_img_list.sort()
    m_img_list = get_listdir(r'H:\PRM\image_580_nii\e_lung')
    m_img_list.sort()
    path = r'H:\PRM\image_580_nii\registration_e2i'

    for i in trange(59, len(f_img_list)):
        _, fullflname = os.path.split(m_img_list[i])

        # Get params and change a few values
        params = pyelastix.get_default_params()
        params.MaximumNumberOfIterations = 600
        params.FinalGridSpacingInVoxels = 10
        params.DefaultPixelValue = -1000
        save_path = os.path.join(path, fullflname + '.txt')
        try:
            im1_deformed, field = pyelastix.register(m_img_list[i], f_img_list[i], params, verbose=0,
                                                     TransformParameters_path=save_path)
            sitk_img = sitk.ReadImage(f_img_list[i])
            new_img = sitk.GetImageFromArray(im1_deformed)
            new_img.SetDirection(sitk_img.GetDirection())
            new_img.SetSpacing(sitk_img.GetSpacing())
            new_img.SetOrigin(sitk_img.GetOrigin())
            sitk.WriteImage(new_img, os.path.join(path, fullflname))
        except:
            print('错误！')
