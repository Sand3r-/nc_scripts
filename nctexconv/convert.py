import argparse, json, os, subprocess
from image_loading import *

def parse_args():
    description = "Nightmare Creatures Texture Conversion tool."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-n', '--names', 
                        dest='texture_names', 
                        metavar='texture_name', 
                        type=str, 
                        nargs='+',
                        help='list of texture names to be converted to .ktx')
    parser.add_argument('-p', '--set-vrml-path', 
                        type=str, 
                        metavar='vrml_path',
                        help='sets path to the folder with Color and Alpha maps',
                        dest='vrml_path')

    args = parser.parse_args()

    if args.vrml_path:
        with open("config.json", "w") as f:
            json.dump({"VrmlPath": args.vrml_path}, f, indent=4)
    
    return args.texture_names

def get_vrml_path():
    with open("config.json", "r") as f:
        config = json.load(f)
        vrml_path = config["VrmlPath"]
    return vrml_path

def create_pair_list(names):
    names = [tex.replace("_c", "") for tex in names]
    result = []
    for name in names:
        color_name = name + "_c.bmp"
        alpha_name = name + "_a.bmp"
        result.append((color_name, alpha_name))
    return result

def convert_files(src_dir, out_dir, names, src_extension, dst_extension, format):
    etc_args = [None] * 6
    etc_args[0] = "EtcTool.exe"
    etc_args[3] = "-m 7"
    etc_args[4] = "-effort 100"
    for name in names:
        etc_args[1] = '\"' + os.path.join(src_dir, name + src_extension) + '\"'
        etc_args[2] = "-format " + format
        etc_args[5] = "-output " + os.path.join(out_dir, name + dst_extension)
        subprocess.run(" ".join(etc_args))
        print("Converted " + name + dst_extension)

def convert(vrml_path, out_dir, opaque_names, transparent_names):
    convert_files(vrml_path, out_dir, opaque_names, ".bmp", ".ktx", "RGB8")
    convert_files(out_dir, out_dir, transparent_names, ".rgb8a1.png", ".rgb8a1.ktx", "RGB8A1")

def main():
    texture_names = parse_args()
    vrml_path = get_vrml_path()
    pair_list = create_pair_list(texture_names)
    out_dir = "output/"
    transparent_names, opaque_names = \
        merge_color_with_alpha_and_save_if_transparent(
            vrml_path, pair_list, out_dir, True)
    convert(vrml_path, out_dir, opaque_names, transparent_names)
    
if __name__ == '__main__':
    main()