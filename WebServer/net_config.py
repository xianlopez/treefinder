import os
import tools


class PredictConfiguration:
    model_name = 'vgg16'  # 'vgg16', 'mnistnet', 'yolo'
    # weights_file = r'.\weights\YOLO_small.ckpt'
    # weights_file = r'.\weights\vgg_16.ckpt'
    weights_file = '/home/xian/brainlab/experiments/2018/2018_05_01_2/model-3'


    ##################################
    ########### PREPROCESS ###########
    class PreprocessOpts:
        type = 'subtract_mean'  # 'fit_to_range', 'subtract_mean'
        range_min = 0
        range_max = 0.4366
        mean = 'vgg'
    preprocess_opts = PreprocessOpts()
    ##################################


    ##################################
    ############ RESIZING ############
    # Select the way to fit the image to the size required by the network.
    # For DETECTION, use ONLY RESIZE_WARP.
    # 'resize_warp': Resize both sides of the image to the required sizes. Aspect ratio may be changed.
    # 'resize_pad_zeros': Scale the image until it totally fits inside the required shape. We pad with zeros the areas
    #                     in which there is no image. Aspect ratio is preserved.
    # 'resize_lose_part': Scale the image until it totally covers the area that the network will see. We may lose the
    #                     upper and lower parts, or the left and right ones. Aspect ratio is preserved.
    # 'centered_crop': Take a centered crop of the image. If any dimension of the image is smaller than the input
    #                  size, we pad with zeros.
    resize_method = 'resize_warp'  # 'resize_warp', 'resize_pad_zeros', 'resize_lose_part', 'centered_crop'
    ##################################

    write_images = True
    write_results = True

    dataset_info_path = '/home/xian/datasets/dataset_arbores_3/dataset_info.xml'
    # dataset_info_path = r'D:\datasets\coco-animals\dataset_info.xml'
    # image_path = [r'C:\Users\xlopez\Desktop\cat.jpg']
    image_path = ['/home/xian/Pictures/IMG_20180414_172848.jpg',
                  '/home/xian/Pictures/IMG_20180414_172853.jpg']
    # image_path = r'D:\datasets\coco-animals\val\horse\COCO_val2014_000000492407.jpg'

    # Options only for detection:
    grid_size = 7  # The amount of horizontal (and vertical) cells in which we will divide the image
    threshold = 0.2  # Confidence threshold
    nonmaxsup = True  # Non-maximum supression
    threshold_nms = 0.5  # Non-maximum supression threshold
    tf_log_level = 'ERROR'
    nsteps_display = 20
    ##################################
    # YOLO CONFIG
    class YoloConfig:
        grid_size = 7
        boxes_per_cell = 2
        image_size = 448
        object_scale = 1.0
        noobject_scale = 1.0
        class_scale = 2.0
        coord_scale = 5.0
    yolo_config = YoloConfig()
    ##################################

    num_workers = 4  # Number of parallel processes to read the data.
    experiments_folder = r'.\experiments'
    random_seed = 1234  # An integer number, or None in order not to set the random seed.
    buffer_size = 1000

    # The following code should not be touched:
    percent_of_data = 100
    initialization_mode = 'load-pretrained'
    # modified_scopes = []
    # modified_scopes = ['vgg_16/fc8']  #
    modified_scopes = []
    batch_size = 1
    outdir = None
    if experiments_folder[0] == '.':  # Relative path
        experiments_folder = tools.join_paths(os.path.dirname(os.path.abspath(__file__)), experiments_folder[2:])
