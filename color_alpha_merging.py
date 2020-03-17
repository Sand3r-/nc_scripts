import sys, cv2
from file_parsing import *
from image_loading import *
from skimage.metrics import structural_similarity as ssim
from operator import itemgetter

if len(sys.argv) < 2:
    print("That ain't no good m8")
    exit()

def str2bool(string):
    return string.lower() == "true"

bmp_dir = sys.argv[1]
save_imgs = False
print("BMP Directory: " + bmp_dir)
if len(sys.argv) > 3:
    save_imgs = str2bool(sys.argv[3])
    print("Save images: " + str(save_imgs))

if len(sys.argv) > 4:
    out_dir = sys.argv[4]
    print("Out Directory: " + out_dir)
else:
    out_dir = "output/"

bmp_filenames = build_file_list(bmp_dir)
bmp_filename_pairs = find_bmp_pairs(bmp_filenames)
merge_color_with_alpha_and_save_if_transparent(bmp_dir, bmp_filename_pairs, out_dir)