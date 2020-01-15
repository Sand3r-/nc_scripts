import os, cv2

def load_cv_image(bmp_dir, filename, cv_flag):
    path = os.path.join(bmp_dir, filename)
    image = cv2.imread(path, cv_flag)
    return image

def get_combined_color_and_alpha(bmp_dir, color_filename, alpha_filename):
    color_img = load_cv_image(bmp_dir, color_filename, cv2.IMREAD_COLOR)
    alpha_img = load_cv_image(bmp_dir, alpha_filename, cv2.IMREAD_GRAYSCALE)

    b_channel, g_channel, r_channel = cv2.split(color_img)
    image = cv2.merge((b_channel, g_channel, r_channel, alpha_img))
    return image

def merge_color_with_alpha_images(bmp_dir, file_pairs, save_imgs):
    images = []
    for color_filename, alpha_filename in file_pairs:
        image = get_combined_color_and_alpha(bmp_dir, color_filename, alpha_filename)
        images.append(image)

        if save_imgs:
            cv2.imwrite(bmp_dir + color_filename[:-len(".bmp")] + ".png", img_BGRA)
    return images

def read_png_images(png_dir, filenames):
    images = []
    for filename in filenames:
        img = load_cv_image(png_dir, filename, cv2.IMREAD_UNCHANGED)
        images.append(img)
    return images