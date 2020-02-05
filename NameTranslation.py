import sys, cv2
from file_parsing import *
from image_loading import *
from skimage.metrics import structural_similarity as ssim
from operator import itemgetter

if len(sys.argv) < 3:
    print("That ain't no good m8")
    exit()

def str2bool(string):
    return string.lower() == "true"

bmp_dir = sys.argv[1]
png_dir = sys.argv[2]
save_imgs = False
print("BMP Directory: " + bmp_dir)
print("PNG Directory: " + png_dir)
if len(sys.argv) > 3:
    save_imgs = str2bool(sys.argv[3])
    print("Save images: " + str(save_imgs))

bmp_filenames = build_file_list(bmp_dir)
png_filenames = build_file_list(png_dir)

# print("Files found in BMP Directory:\n" + str(bmp_filenames))

bmp_filename_pairs = find_bmp_pairs(bmp_filenames)

bmp_images = merge_color_with_alpha_images(bmp_dir, bmp_filename_pairs, save_imgs)
png_images = read_png_images(png_dir, png_filenames)

ssim_mtx = []

for bmp_file, bmp in bmp_images:
    bmp_record = []
    for png_file, png in png_images:
        bmp_record.append((png_file, ssim(bmp, png, multichannel=True)))
    ssim_mtx.append((bmp_file, bmp_record))

uncertain_matches = []
certain_matches = []
# Parse the results
for file, lists in ssim_mtx:
    match, highest_probability = max(lists,key=itemgetter(1))
    if highest_probability < 0.9:
        uncertain_matches.append((file, match, highest_probability))
    else:
        certain_matches.append((file, match, highest_probability))
        # print(file + " cannot be surely assigned to any other picture")
        # print("The best match is " + match)
        # print("Probability: " + highest_probability)

print("Certain:")
for file, match, prob in certain_matches:
    print(file, "- " + match)

if len(uncertain_matches) > 0:
    uncertain_matches = sorted(uncertain_matches, key=itemgetter(2))
    print("Some matches cannot be surely assigned to another picture.")
    print("Each is presented with probable pair and its probability.")
    print("Uncertain:")
    for file, match, prob in uncertain_matches:
        print(file, "- " + match + "- " + str(prob))