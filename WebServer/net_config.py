import os
import tools


class PredictConfiguration:
    model_name = 'vgg16'  # 'vgg16', 'mnistnet', 'yolo'
    # weights_file = r'.\weights\YOLO_small.ckpt'
    # weights_file = r'.\weights\vgg_16.ckpt'
    weights_file = '/home/xian/brainlab/experiments/2018/vgg_arbores_3/model-15'


    ##################################
    ########### PREPROCESS ###########
    class PreprocessOpts:
        type = 'subtract_mean'  # 'fit_to_range', 'subtract_mean'
        range_min = 0
        range_max = 0.4366
        mean = 'vgg'
    preprocess_opts = PreprocessOpts()
    ##################################

    dropout_keep_prob = 1.0
    gpu_memory_fraction = 0.5

    ##################################
    ############ RESIZING ############
    resize_method = 'resize_warp'  # 'resize_warp', 'resize_pad_zeros', 'resize_lose_part', 'centered_crop'
    ##################################

    write_images = True
    write_results = True

    dataset_info_path = '/home/xian/datasets/arbores_2018-05-30_00-09/dataset_info.xml'
    image_path = []
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
    experiments_folder = './experiments'
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
