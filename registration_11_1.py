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
    f_img_list = get_listdir(r'H:\PRM\59_cases_nii\59_cases_nii_i_lung')
    f_img_list.sort()
    m_img_list = get_listdir(r'H:\PRM\59_cases_nii\registration_e2i\output_0')
    m_img_list.sort()
    path = r'H:\PRM\59_cases_nii\registration_e2i\output_1'
    # 007 011 016
    for i in trange(len(f_img_list)):
        _, fullflname = os.path.split(m_img_list[i])

        # Get params and change a few values
        params = pyelastix.get_default_params()

        FixedInternalImagePixelType = "float"
        FixedImageDimension = 3
        MovingInternalImagePixelType = "float"
        MovingImageDimension = 3

        Registration = "MultiMetricMultiResolutionRegistration"
        FixedImagePyramid = "FixedRecursiveImagePyramid"
        MovingImagePyramid = "MovingRecursiveImagePyramid"
        Interpolator = "BSplineInterpolator"
        Metric = ("AdvancedNormalizedCorrelation", "TransformBendingEnergyPenalty")
        Optimizer = "AdaptiveStochasticGradientDescent"
        ResampleInterpolator = "FinalBSplineInterpolator"
        Resampler = "DefaultResampler"
        Transform = "BSplineTransform"

        NumberOfResolutions = 5
        ImagePyramidSchedule = (16, 16, 16, 8, 8, 8, 4, 4, 4, 2, 2, 2, 1, 1, 1)

        FinalGridSpacingInPhysicalUnits = (10.0, 10.0, 10.0)
        GridSpacingSchedule = (8.0, 8.0, 4.0, 2.0, 1.0)
        HowToCombineTransforms = "Compose"

        MaximumNumberOfIterations = 1000

        AutomaticParameterEstimation = "true"
        UseAdaptiveStepSizes = "true"

        UseRelativeWeights = "true"
        Metric0RelativeWeight = 1.0
        Metric1RelativeWeight = 0.05

        WriteTransformParametersEachIteration = "false"
        WriteTransformParametersEachResolution = "true"
        WriteResultImageAfterEachResolution = "false"
        WritePyramidImagesAfterEachResolution = "false"
        WriteResultImage = "false"
        ShowExactMetricValue = "false"
        ErodeMask = "false"
        UseDirectionCosines = "true"

        ImageSampler = "RandomCoordinate"
        NumberOfSpatialSamples = 2000
        NewSamplesEveryIteration = "true"
        UseRandomSampleRegion = "false"
        SampleRegionSize = (50.0, 50.0, 50.0)
        MaximumNumberOfSamplingAttempts = 50

        BSplineInterpolationOrder = 1

        FinalBSplineInterpolationOrder = 3

        params.DefaultPixelValue = 0  # TODO：需要修改
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
            print(m_img_list[i] + ' 错误！')
