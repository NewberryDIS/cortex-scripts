from PIL import Image
import os, sys

output_list = []

input_dir = sys.argv[1]
output_dir = sys.argv[2]
# print(input_dir)
# print(output_dir)
for root, dirs, files in os.walk(input_dir):
    for fn in files:
        # print(fn)
        infile = os.path.join(root, fn)
        output_path = root.replace(input_dir, output_dir)
        outfile = os.path.join(output_path, fn)
        image = Image.open(infile)
        mkdir_command = 'if not exist "' + output_path + '" md /S "' + output_path + '"'
        # mkdir_command = 'mkdir -p ' + output_path
        output_list.append(mkdir_command)
        if image.width > image.height:
            
            slice_command = '"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\convert.exe" +adjoin -quiet -crop 2x1@ +repage "' + infile + '" "' + os.path.join(output_path, fn.replace('.TIF','-%01d.TIF')) + '"'
            # slice_command = 'convert +adjoin -quiet -crop 50%x100% "' + infile + '" "' + os.path.join(output_path, fn.replace('.TIF','-%01d.TIF')) + '"'
            output_list.append(slice_command)
        else: 
            copy_command = 'copy "' + infile + '" "' + os.path.join(output_path, fn) + '"'
            # copy_command = 'cp -vi ' + infile + ' ' + os.path.join(output_path, fn)
            output_list.append(copy_command)

with open('slicer_script.bat', 'w') as fp:
    for line in output_list:
        fp.write("%s\n" % line)
