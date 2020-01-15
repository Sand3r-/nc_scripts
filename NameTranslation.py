import sys, cv2
from file_parsing import *
from image_loading import *

if len(sys.argv) < 3:
    print("That ain't no good m8")
    exit()

def str2bool(string):
    return string.lower() == "true"

bmp_dir = sys.argv[1]
png_dir = sys.argv[2]
print("BMP Directory: " + bmp_dir)
print("PNG Directory: " + png_dir)
if len(sys.argv) > 3:
    save_imgs = str2bool(sys.argv[3])
    print("Save images: " + str(save_imgs))

bmp_filenames = build_file_list(bmp_dir)
png_filenames = build_file_list(png_dir)

print("Files found in BMP Directory:\n" + str(bmp_filenames))

bmp_filename_pairs = find_bmp_pairs(bmp_filenames)

bmp_images = merge_color_with_alpha_images(bmp_dir, bmp_filename_pairs, save_imgs)
png_images = read_png_images(png_dir, png_filenames)