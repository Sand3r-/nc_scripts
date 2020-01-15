import os

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