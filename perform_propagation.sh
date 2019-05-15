GPUID=0
CONFIG='./configs/config_camvid360.json'
SOURCE_IMAGE='./sample_outputs/camvid360/images_binary/R0010094_20170622125256_er_f_00008010.bin'

python ./scripts/experiment_launch_propagation.py $CONFIG $GPUID $SOURCE_IMAGE
