# data-rescue
磁盘不能打开，数据救援，数据备份

## python3.11

## 依赖包
`pytsk3`


## 具体操作 on MacBook Air(M1)
- 查看磁盘（包括未挂载的磁盘）
    ```commandline
    diskutil list
    ```
  
  + FDisk_partition_scheme 磁盘分区方案
  + Windows_FAT_32 表示分区文件系统
  + IDENTIFIER 磁盘或分区标识
> `FAT32` 是一种常见的文件系统，通常用于跨平台的可移动存储设备。

- 查看磁盘信息
    > 选择`FAT32`所对应的标识
    ```commandline
    diskutil info /dev/disk4s1
    ```

## 问题
 - Error: Img_Info_Con: (tsk3.cpp:103) Unable to open image: Error opening image file (raw_open: file "/dev/disk4" - Permission denied)
   - 使用Terminal, sudo运行, ` sudo python3 main.py`
 - Error: FS_Info_Con: (tsk3.cpp:214) Unable to open the image as a filesystem at offset: 0x00193f00 with error: Possible encryption detected (High entropy (8.00))
   > 文件系统被加密了
 - Error: FS_Info_Con: (tsk3.cpp:214) Unable to open the image as a filesystem at offset: 0x00000800 with error: Invalid magic value (Error: sector size (0) is not a multiple of device size (512)
Do you have a disk image instead of a partition image?)
   > 暂无解决办法