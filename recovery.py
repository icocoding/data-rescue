import os

import pytsk3

from pytsk3 import File


def get_file_name(entry: File):
    """
    从目录项中获取文件名

    参数:
    - entry: pytsk3 目录项对象

    返回:
    - 文件名（字符串）
    """
    try:
        name = entry.info.name.name.decode('utf-8')
    except Exception as e:
        try:
            name = entry.info.name.name.decode('ios-8859-1')
        except Exception as e1:
            name = "unknown"

    return name


def skip_file_name_to_iterate(file_name):
    return file_name in ['.', '..', '_', '.0$^!', 'unknown']


def backup_file(backup_dir, dir_path, file_name, file_size, filesystem_handle):
    file_path = f"{dir_path}/{file_name}"
    destination_dir = f"{backup_dir}{dir_path}"
    print(f"copy {file_path} to {destination_dir}")
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 获取文件句柄
    file_handle: File = filesystem_handle.open(file_path)

    # 将文件数据写入备份文件夹中的文件
    destination_path = os.path.join(destination_dir, file_name)

    # 写入数据
    buffer_size = 4096
    with open(destination_path, 'wb') as backup_file:
        # 读取文件数据
        try:
            for i in range(0, int(file_size / buffer_size) + 1):
                file_data = file_handle.read_random(buffer_size * i, buffer_size)
                if file_data is not None:
                    backup_file.write(file_data)
            print(f"success")
        except Exception as e:
            print(f"error: {e}")

    # 获取文件的元信息
    file_stat = os.stat(file_path)

    # 获取文件原有的元信息字典
    # existing_metadata = os.stat(file_path).st_atime // 最后访问时间
    # existing_metadata = os.stat(file_path).st_ctime // 文件状态更改时间
    # existing_metadata = os.stat(file_path).st_mtime // 文件修改时间
    # st_birthtime

    os.utime(destination_path, times=(file_stat.st_atime, file_stat.st_mtime))


def list_files_in_dir(dir_path, filesystem_handle, only_list_files, backup_dir):
    dir_used_size = 0
    try:
        # 获取目录
        directory: pytsk3.Directory = filesystem_handle.open_dir(dir_path, 2)

        print(f'dir: {dir_path} size: {directory.size}')

        # 遍历根目录的条目
        for entry in directory:
            file_name = get_file_name(entry)
            file_size: int = entry.info.meta.size  # 获取文件的绝对路径
            file_path = f"{dir_path}/{file_name}"

            # 计算目录文件大小
            dir_used_size += file_size

            # 判断是否为文件夹
            is_directory = entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR

            print(f"File: {file_path} Size: {file_size} DIR: {is_directory}")

            # 备份文件
            if not only_list_files and not is_directory:
                backup_file(backup_dir, dir_path, file_name, file_size, filesystem_handle)

            # 递归遍历目录
            # 排除 . 或 ..
            if is_directory and not skip_file_name_to_iterate(file_name):
                dir_used_size += list_files_in_dir(f'{file_path}', filesystem_handle, only_list_files, backup_dir)

        return dir_used_size

    except Exception as e:
        print(f"Error: {e}")


def try_to_read_data(disk_path, offset):
    try:
        # 打开磁盘
        image_handle = pytsk3.Img_Info(disk_path)
        print(f'opened: {disk_path}')
        # 磁盘类型 , type=pytsk3.TSK_FS_TYPE_NTFS
        # FAT32：type=pytsk3.TSK_FS_TYPE_FAT32
        filesystem_handle = pytsk3.FS_Info(image_handle, offset=offset,
                                           type=pytsk3.TSK_FS_TYPE_EXT4)

        print(f'FS_Info: {disk_path}')
        image_handle.close()
    except Exception as e:
        print(f"Error: {e}")


def recovery_files_on_disk(disk_path, rescue_path, offset=0, back_up_dir=None, only_list_files=False):
    """
    从磁盘中恢复文件或列出文件

    参数:
    - disk_path: 磁盘映像文件路径
    - rescue_path: 恢复文件的目标目录路径
    - back_up_dir: 备份文件的目录路径（可选）
    - only_list_files: 是否仅列出文件而不进行备份（默认为False）

    无返回值，直接在控制台输出信息
    """
    try_to_read_data(disk_path, offset)
    try:
        # 打开磁盘
        image_handle = pytsk3.Img_Info(disk_path)
        print(f'opened: {disk_path}')
        # 磁盘类型 , type=pytsk3.TSK_FS_TYPE_NTFS
        # FAT32：type=pytsk3.TSK_FS_TYPE_FAT32
        filesystem_handle = pytsk3.FS_Info(image_handle, offset=offset
                                           # ,type=pytsk3.TSK_FS_TYPE_FAT32
                                           )
        print(f'FS_Info: {disk_path}')
        if back_up_dir is None:
            only_list_files = True

        # 获取目录, 并计算文件大小
        disk_used_size = list_files_in_dir(rescue_path, filesystem_handle, only_list_files, back_up_dir)

        print(f"{rescue_path} size: {disk_used_size / 1024 / 1024}M")

    except Exception as e:
        print(f"Error: {e}")
