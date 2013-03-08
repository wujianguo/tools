#! /bin/bash
#开机自动挂载windows硬盘
rmdir /mnt/*
umount -a
for WINPAN in `fdisk -l |grep "NTFS" |cut -d ' ' -f1 |cut -d / -f3`
do
	if   test ! -d /mnt/$WINPAN 
	then
		mkdir "/mnt/$WINPAN"
	fi
	mount /dev/$WINPAN /mnt/$WINPAN -o iocharset=gb2312,codepage=936
done
#for WINPAN2 in `fdisk -l |grep "FAT" |cut -d ' ' -f1 |cut -d / -f3`
#do
#	if   test ! -d /mnt/$WINPAN2 
#	then
#		mkdir "/mnt/$WINPAN2"
#	fi
#	echo "ok"
#	mount /dev/$WINPAN2 /mnt/$WINPAN2  -o exec,dev,suid,rw,iocharset=gb2312,codepage=936
#done
#mount --bind /mnt/sda8/我的资料/计算机 /home/justin/ftp/computerdata
#mount --bind /mnt/sdb3/games /home/justin/ftp/games
#mount --bind /mnt/sdb3/iso /home/justin/ftp/iso/iso1
#mount --bind /mnt/sda6/iso /home/justin/ftp/iso/iso2
#mount --bind /mnt/sdb3/linux /home/justin/ftp/linux
#mount --bind /mnt/sda7/电影 /home/justin/ftp/movie
#mount --bind /mnt/sda7/音乐 /home/justin/ftp/music
#mount --bind /mnt/sda6/computer /home/justin/ftp/video
#mount --bind /mnt/sdc3/windows /home/justin/ftp/winsoft
#mount --bind /mnt/sdc3/synt /home/justin/sync
