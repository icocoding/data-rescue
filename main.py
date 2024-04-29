import os
import sys

from recovery import recovery_files_on_disk
from DiskUtil import list_partitions, read_deleted_data

# 请替换为你未挂载磁盘的设备路径
disk_path = '/dev/diskxxx'  # 示例路径，替换为实际路径

# 请替换需要恢复的数据目录, 磁盘的相对路径
rescue_path = '/myfiles'

# 数据恢复的备份目录
back_up_dir = '/Volumes/backup'


def check_sudo_privileges():
    # 尝试执行一个不需要root权限但可能需要sudo权限的命令
    try:
        os.system("sudo -n true")
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    # 使用sudo命令请求root权限
    # os.system("sudo python3 {}".format(" ".join(sys.argv)))
    # 在需要sudo权限的代码块前检查权限
    if not check_sudo_privileges():
        sys.exit("You need to have sudo privileges to run this script.")
    else:
        print("no permission")
        pass
    # 使用os.setuid请求root权限
    # os.setuid(0)
    # 恢复备份 rescue_path 文件
    # recovery_files_on_disk()
    # read_deleted_data('/dev/disk6s1')
    list_partitions('/dev/disk4')
    # 列出 rescue_path 下的文件，可以设置 rescue_path = '/'
    recovery_files_on_disk('/dev/disk4', '/', 1654528,
                           # , back_up_dir
                           # , True
                           )
