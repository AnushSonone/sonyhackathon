# This file creates a csv file enlisting all images in the archive folder

import sys
import os.path

if __name__ == "__main__":
    f = open("archive.txt", "w")

    path = "archive"
    label = 0
    separator = ";"
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                # print(abs_path, separator, label)
                f.write(abs_path + separator + str(label) + "\n")
            label = label + 1
    f.close()
