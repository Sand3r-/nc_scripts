import argparse, json, os, subprocess, sys
from nctexconv.image_loading import *

cfg_path = os.path.join(os.path.dirname(__file__), "config.json")

def save_cfg_path(path, cfg_entry_name, printed_name):
    if path:
        if not os.path.isabs(path):
            print("Provided " + printed_name + " is not absolute. Please provide an absolute path")
            print(path)
            exit(-1)
        with open(cfg_path, "r") as f:
            config = json.load(f)
        with open(cfg_path, "w") as f:
            config[cfg_entry_name] = path
            json.dump(config, f, indent=4)
        print(printed_name + " set to " + path)

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
    parser.add_argument('-o', '--set-output-path', 
                        type=str, 
                        metavar='output_path',
                        help='sets path to the ktx output folder',
                        dest='output_path')

    args = parser.parse_args()

    save_cfg_path(args.vrml_path, "VrmlPath", "VRML path")
    save_cfg_path(args.output_path, "OutputPath", "Output path")
    
    if len(sys.argv) < 2:
        parser.print_help()

    if args.texture_names is None:
        exit()

    return args.texture_names

def get_src_dst_paths():
    with open(cfg_path, "r") as f:
        config = json.load(f)
        vrml_path = config["VrmlPath"]
        out_path = config["OutputPath"]
    return vrml_path, out_path

def create_pair_list(names):
    names = [tex.replace("_c", "") for tex in names]
    result = []
    for name in names:
        color_name = name + "_c.bmp"
        alpha_name = name + "_a.bmp"
        result.append((color_name, alpha_name))
    return result

def convert_files(src_dir, out_dir, names, src_extension, dst_extension, format):
    etc_args = [None] * 12
    etc_args[0] = "EtcTool.exe"
    etc_args[4] = "-m"
    etc_args[5] = "7"
    etc_args[6] = "-effort"
    etc_args[7] = "100"
    etc_args[8] = "-j"
    etc_args[9] = "6"
    for name in names:
        etc_args[1] = os.path.join(src_dir, name + src_extension)
        etc_args[2] = "-format"
        etc_args[3] = format
        etc_args[10] = "-output"
        etc_args[11] = out_dir + "/" + name + dst_extension
        result = subprocess.run(etc_args, shell=True, capture_output=True, universal_newlines=True)
        print(result.stdout)
        print(result.stderr)
        print("Converted " + name + dst_extension)

def convert(vrml_path, out_dir, opaque_names, transparent_names):
    convert_files(vrml_path, out_dir, opaque_names, ".bmp", ".ktx", "RGB8")
    convert_files(out_dir, out_dir, transparent_names, ".rgb8a1.png", ".rgb8a1.ktx", "RGB8A1")

def main():
    texture_names = parse_args()
    vrml_path, out_dir = get_src_dst_paths()
    pair_list = create_pair_list(texture_names)
    transparent_names, opaque_names = \
        merge_color_with_alpha_and_save_if_transparent(
            vrml_path, pair_list, out_dir, True)
    convert(vrml_path, out_dir, opaque_names, transparent_names)
    
if __name__ == '__main__':
    main()