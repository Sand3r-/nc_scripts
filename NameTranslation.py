import sys, os, cv2

if len(sys.argv) < 3:
    print("That ain't no good m8")
    exit()

def str2bool(string):
    return string.lower() == "true"

def build_file_list(dir):
    result = []
    for root, directories, files in os.walk(dir):
        for file in files:
            result.append(file)
    return result

def filter_color_bmps(filenames):
    result = list(filter(lambda filename: "_c.bmp" in filename, filenames))
    print("Filtered Color BMPs:")
    print(result)
    return result

def filter_alpha_bmps(filenames):
    result = list(filter(lambda filename: "_a.bmp" in filename, filenames))
    print("Filtered Alpha BMPs:")
    print(result)
    return result

def color2alpha_filename(color_filename):
    result = color_filename.replace("_c.bmp", "_a.bmp")
    print("Generated alpha name:")
    print(result)
    return result

def append_pair_if_alpha_exists(result, color_filename, alpha_bmps):
    desired_alpha_filename = color2alpha_filename(color_filename)
    if desired_alpha_filename in alpha_bmps:
        result.append((color_filename, desired_alpha_filename))
    else:
        print("No alpha bmp found for color file + ", color_filename)

def create_bmp_pair_list(color_bmps, alpha_bmps):
    result = []
    for color_filename in color_bmps:
        append_pair_if_alpha_exists(result, color_filename, alpha_bmps)
    return result

def find_bmp_pairs(filenames):
    color_bmps = filter_color_bmps(filenames)
    alpha_bmps = filter_alpha_bmps(filenames)

    result = create_bmp_pair_list(color_bmps, alpha_bmps)
    print("Found color, alpha pairs:")
    print(result)
    return result


def load_cv_image(bmp_dir, filename, cv_flag):
    path = os.path.join(bmp_dir, filename)
    image = cv2.imread(path, cv_flag)
    return image

def merge_color_with_alpha_images(bmp_dir, file_pairs):
    images = []
    for color_filename, alpha_filename in file_pairs:
        color_img = load_cv_image(bmp_dir, color_filename, cv2.IMREAD_COLOR)
        alpha_img = load_cv_image(bmp_dir, alpha_filename, cv2.IMREAD_GRAYSCALE)

        b_channel, g_channel, r_channel = cv2.split(color_img)
        # alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_img))
        images.append(img_BGRA)
        global save_imgs
        if save_imgs:
            cv2.imwrite(bmp_dir + color_filename[:-len(".bmp")] + ".png", img_BGRA)
    return images

def read_png_images(png_dir, filenames):
    images = []
    for filename in filenames:
        img = load_cv_image(png_dir, filename, cv2.IMREAD_UNCHANGED)
        images.append(img)
    return images

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

bmp_images = merge_color_with_alpha_images(bmp_dir, bmp_filename_pairs)
png_images = read_png_images(png_dir, png_filenames)