# coding=utf-8
import os

INPUT_PATH_LEFT = "./input/1/"
INPUT_PATH_RIGHT = "./input/2/"

if __name__ == '__main__':
    # 文件结构转化为bc folder compare输出的结果
    # 构建dir_list_left和dir_list_right，按顺序插入dir_ele，dir_ele包括path和files
    dir_list_left = []
    dir_list_right = []
    for root, dirs, files in os.walk(INPUT_PATH_LEFT):
        root = root.replace(INPUT_PATH_LEFT, "")
        if root != "" and not root.endswith("/"):
            root = root + "/"
        dir_ele = {}
        dir_ele["path"] = root
        dir_ele["files"] = []
        for name in files:
            dir_ele["files"].append(root+name)
        dir_list_left.append(dir_ele)
    for root, dirs, files in os.walk(INPUT_PATH_RIGHT):
        root = root.replace(INPUT_PATH_RIGHT, "")
        if root != "" and not root.endswith("/"):
            root = root + "/"
        dir_ele = {}
        dir_ele["path"] = root
        dir_ele["files"] = []
        for name in files:
            dir_ele["files"].append(root+name)
        dir_list_right.append(dir_ele)
    # 比较dir_list_left和dir_list_right，生成file_list。file_list中目录和文件的顺序同bc folder compare输出的结果
    # file_list的元素为file_ele，包括leftOrRight, isDIr, leftFile, rightFile
    file_list = []
    index_left = 0
    index_right = 0
    while index_left < len(dir_list_left) and index_right < len(dir_list_right):
        dir_left = dir_list_left[index_left]["path"]
        dir_right = dir_list_right[index_right]["path"]
        if dir_left == dir_right:   # file_list中插入的dir两侧都有
            # file_list中插入dir
            file_ele = {}
            file_ele["isDir"] = True
            file_ele["leftOrRight"] = "both"
            file_ele["leftFile"] = dir_left
            file_ele["rightFile"] = dir_right
            file_list.append(file_ele)
            # file_list中插入dir下的files
            # 需要比较dir_left和dir_right下的文件
            files_in_dir_left = dir_list_left[index_left]["files"]
            files_in_dir_right = dir_list_right[index_right]["files"]
            index_file_left = 0
            index_file_right = 0
            while index_file_left < len(files_in_dir_left) and index_file_right < len(files_in_dir_right):
                file_left = files_in_dir_left[index_file_left]
                file_right = files_in_dir_right[index_file_right]
                if file_left == file_right:
                    file_ele = {}
                    file_ele["isDir"] = False
                    file_ele["leftOrRight"] = "both"
                    file_ele["leftFile"] = file_left
                    file_ele["rightFile"] = file_right
                    file_list.append(file_ele)
                    ###############
                    # generate html
                    ###############
                    index_file_left += 1
                    index_file_right += 1
                elif file_left < file_right:
                    file_ele = {}
                    file_ele["isDir"] = False
                    file_ele["leftOrRight"] = "left"
                    file_ele["leftFile"] = file_left
                    file_ele["rightFile"] = None
                    file_list.append(file_ele)
                    ###############
                    # generate html
                    ###############
                    index_file_left += 1
                else:
                    file_ele = {}
                    file_ele["isDir"] = False
                    file_ele["leftOrRight"] = "right"
                    file_ele["leftFile"] = None
                    file_ele["rightFile"] = file_right
                    file_list.append(file_ele)
                    ###############
                    # generate html
                    ###############
                    index_file_right += 1
            # 插入剩下的文件
            while index_file_left < len(files_in_dir_left):
                file_ele = {}
                file_ele["isDir"] = False
                file_ele["leftOrRight"] = "left"
                file_ele["leftFile"] = files_in_dir_left[index_file_left]
                file_ele["rightFile"] = None
                file_list.append(file_ele)
                index_file_left += 1
            while index_file_right < len(files_in_dir_right):
                file_ele = {}
                file_ele["isDir"] = False
                file_ele["leftOrRight"] = "right"
                file_ele["leftFile"] = None
                file_ele["rightFile"] = files_in_dir_right[index_file_right]
                file_list.append(file_ele)
                index_file_right += 1
            # increment index
            index_left += 1
            index_right += 1
        elif dir_left < dir_right:  # file_list中插入的dir只有左侧有
            # file_list中插入dir
            file_ele = {}
            file_ele["isDir"] = True
            file_ele["leftOrRight"] = "left"
            file_ele["leftFile"] = dir_left
            file_ele["rightFile"] = None
            file_list.append(file_ele)
            # file_list中插入dir下的files
            for filename in dir_list_left[index_left]["files"]:
                file_ele = {}
                file_ele["isDir"] = False
                file_ele["leftOrRight"] = "left"
                file_ele["leftFile"] = filename
                file_ele["rightFile"] = None
                file_list.append(file_ele)
                ###############
                # generate html
                ###############
            index_left += 1
        else:                       # file_list中插入的dir只有右侧有
            # file_list中插入dir
            file_ele = {}
            file_ele["isDir"] = True
            file_ele["leftOrRight"] = "right"
            file_ele["rightFile"] = dir_right
            file_ele["leftFile"] = None
            file_list.append(file_ele)
            # file_list中插入dir下的files
            for filename in dir_list_right[index_right]["files"]:
                file_ele = {}
                file_ele["isDir"] = False
                file_ele["leftOrRight"] = "right"
                file_ele["rightFile"] = filename
                file_ele["leftFile"] = None
                file_list.append(file_ele)
                ###############
                # generate html
                ###############
            index_right += 1
    # dir_list_left或者dir_list_right有遗留
    while index_left < len(dir_list_left):
        dir_left = dir_list_left[index_left]["path"]
        # file_list中插入dir
        file_ele = {}
        file_ele["isDir"] = True
        file_ele["leftOrRight"] = "left"
        file_ele["leftFile"] = dir_left
        file_ele["rightFile"] = None
        file_list.append(file_ele)
        # file_list中插入dir下的files
        for filename in dir_list_left[index_left]["files"]:
            file_ele = {}
            file_ele["isDir"] = False
            file_ele["leftOrRight"] = "left"
            file_ele["leftFile"] = filename
            file_ele["rightFile"] = None
            file_list.append(file_ele)
            ###############
            # generate html
            ###############
        index_left += 1
    while index_right < len(dir_list_right):
        dir_right = dir_list_right[index_right]["path"]
        # file_list中插入dir
        file_ele = {}
        file_ele["isDir"] = True
        file_ele["leftOrRight"] = "right"
        file_ele["leftFile"] = None
        file_ele["rightFile"] = dir_right
        file_list.append(file_ele)
        # file_list中插入dir下的files
        for filename in dir_list_right[index_right]["files"]:
            file_ele = {}
            file_ele["isDir"] = False
            file_ele["leftOrRight"] = "right"
            file_ele["leftFile"] = None
            file_ele["rightFile"] = filename
            file_list.append(file_ele)
            ###############
            # generate html
            ###############
        index_right += 1
    
    # print(str(dir_list_left))
    # print(str(dir_list_right))
    print(str(file_list))