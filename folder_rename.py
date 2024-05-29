import os

prevtrunk = ''

for top_root, top_dirs, top_files in os.walk('./'):
    for dirname in sorted(top_dirs):
        for inner_root, inner_dir, inner_files in os.walk(dirname):
            for file in sorted(inner_files):
                if file not in ['Thumbs.db', 'rename_folders_firstfile.py', 'test_maker.sh']:
                    print(file)
                    filename_trunk = os.path.splitext(file)[0]
                    try:
                        os.rename(dirname, filename_trunk)
                        prevtrunk = filename_trunk
                    except: 
                        print("headpats for python.  you're ok, python.  everything is fine.  nothing is ruined.")
            print (dirname + " -> " + prevtrunk)
            print( ".         .         .         .         .         .")