
import pytsk3


def list_partitions(disk_path):
    """
    列出磁盘上的分区信息

    参数:
    - disk_path: 磁盘映像文件路径

    返回:
    - 分区信息列表，每个分区表示为字典，包含地址（addr）、起始位置（start）、长度（len）和描述（desc）等信息
    """
    parts = []
    try:
        # 打开 NTFS 硬盘
        ntfs_handle = pytsk3.Img_Info(disk_path)

        # 获取磁盘上的分区表
        partition_table = pytsk3.Volume_Info(ntfs_handle)

        # 遍历分区表
        for partition in partition_table:
            # 获取分区的设备路径
            partition_path = None
            try:
                filesystem_handle = pytsk3.FS_Info(ntfs_handle, offset=partition.start)
                partition_path = filesystem_handle.info.device
            except Exception as e:
                pass
                # print(f"Error getting partition path: {e}")

            p = {'addr': partition.addr, 'start': partition.start, 'len': partition.len, 'desc': partition.desc,
                 'path': partition_path}
            parts.append(p)
            print(p)
        return parts

    except Exception as e:
        print(f"Error: {e}")


def read_deleted_data(disk_path):
    """
    读取磁盘上已删除文件的数据

    参数:
    - disk_path: 磁盘映像文件路径

    无返回值，直接在控制台输出已删除文件的数据
    """
    try:
        # 打开磁盘
        image_handle = pytsk3.Img_Info(disk_path)

        # 打开文件系统
        # type=pytsk3.TSK_FS_TYPE_ENUM.TSK_FS_TYPE_NTFS

        filesystem_handle = pytsk3.FS_Info(image_handle, offset=0)

        # 遍历文件系统
        for fs_object in filesystem_handle.recurse():
            # 检查是否为已删除的文件
            if fs_object.info.meta.flags & pytsk3.TSK_FS_META_FLAG_ALLOC:
                continue  # 跳过已分配的文件

            # 读取已删除文件的内容
            file_data = fs_object.read_random(0, fs_object.info.meta.size, pytsk3.TSK_FS_TYPE_NTFS)

            # 处理已删除文件的数据，例如打印前几个字节
            print(f"Read {len(file_data)} bytes from deleted file: {fs_object.info.name.name.decode('utf-8')}")
            print(file_data[:16])  # 打印前16个字节作为示例

    except Exception as e:
        print(f"Error: {e}")