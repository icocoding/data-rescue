import os

import pytsk3

from pytsk3 import File

# 请替换为你未挂载磁盘的设备路径
disk_path = '/dev/diskxxx'  # 示例路径，替换为实际路径

# 请替换需要恢复的数据目录, 磁盘的相对路径
rescue_path = '/myfiles'

# 数据恢复的备份目录
back_up_dir = '/Volumes/backup'


def recovery_files_on_disk(onlyListFiles=False):
    try:
        # 打开磁盘
        image_handle = pytsk3.Img_Info(disk_path)
        print(f'opened: {disk_path}')
        filesystem_handle = pytsk3.FS_Info(image_handle, offset=0)

        def back_up(dir_path, file_name, file_size):
            file_path = f"{dir_path}/{file_name}"
            destination_dir = f"{back_up_dir}{dir_path}"
            print(f"copy {file_path} to {destination_dir}")
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            # 获取文件句柄
            file_handle: File = filesystem_handle.open(file_path)

            # 将文件数据写入备份文件夹中的文件
            destination_path = os.path.join(destination_dir, file_name)

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

        def list_files_in_dir(dir_path):
            dir_used_size = 0
            try:
                # 获取目录
                directory: pytsk3.Directory = filesystem_handle.open_dir(dir_path, 2)

                print(f'dir: {dir_path} size: {directory.size}')

                # 遍历根目录的条目
                for entry in directory:
                    file_name = entry.info.name.name.decode('utf-8')
                    file_size: int = entry.info.meta.size  # 获取文件的绝对路径
                    file_path = f"{dir_path}/{file_name}"

                    # 计算目录文件大小
                    dir_used_size += file_size

                    # 判断是否为文件夹
                    is_directory = entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR

                    print(f"File: {file_path} Size: {file_size} DIR: {is_directory}")

                    # 备份文件
                    if not onlyListFiles and not is_directory:
                        back_up(dir_path, file_name, file_size)

                    # 递归遍历目录
                    # 排除 . 或 ..
                    if is_directory and (file_name != '.' and file_name != '..'):
                        dir_used_size += list_files_in_dir(f'{file_path}')

                return dir_used_size

            except Exception as e:
                print(f"Error: {e}")

        # 获取目录, 并计算文件大小
        disk_used_size = list_files_in_dir(rescue_path)

        print(f"{rescue_path} size: {disk_used_size / 1024 / 1024}M")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # 恢复备份 rescue_path 文件
    # recovery_files_on_disk()

    # 列出 rescue_path 下的文件，可以设置 rescue_path = '/'
    recovery_files_on_disk(True)
