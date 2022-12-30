import sys
import binascii
import re
import hashlib

partitions = {
'00':'Empty',
'01':'FAT12',
'02':'XENIX root',
'03':'XENIX usr',
'04':'FAT16 <32M',
'05':'Extended',
'06':'FAT16',
'07':'HPFS/NTFS/exFAT',
'08':'AIX',
'09':'AIX bootable',
'0a':'OS/2 Boot Manager',
'0b':'W95 FAT32',
'0c':'W95 FAT32 (LBA)',
'0e':'W95 FAT16 (LBA)',
'0f':"W95 Ext'd (LBA)",
'10':'OPUS',
'11':'Hidden FAT12',
'12':'Compaq diagnost',
'14':'Hidden FAT16 <3',
'16':'Hidden FAT16',
'17':'Hidden HPFS/NTF',
'18':'AST SmartSleep',
'1b':'Hidden W95 FAT3',
'1c':'Hidden W95 FAT3',
'1e':'Hidden W95 FAT1',
'24':'NEC DOS',
'27':'Hidden NTFS Win',
'39':'Plan 9',
'3c':'PartitionMagic',
'40':'Venix 80286',
'41':'PPC PReP Boot',
'42':'SFS',
'4d':'QNX4.x',
'4e':'QNX4.x 2nd part',
'4f':'QNX4.x 3rd part',
'50':'OnTrack DM',
'51':'OnTrack DM6 Aux',
'52':'CP/M',
'53':'OnTrack DM6 Aux',
'54':'OnTrackDM6',
'55':'EZ-Drive',
'56':'Golden Bow',
'5c':'Priam Edisk',
'61':'SpeedStor',
'63':'GNU HURD or Sys',
'64':'Novell Netware',
'65':'Novell Netware',
'70':'DiskSecure Mult',
'75':'PC/IX',
'80':'Old Minix',
'81':'Minix / old Lin',
'82':'Linux swap / So',
'83':'Linux',
'84':'OS/2 hidden C:',
'85':'Linux extended',
'86':'NTFS volume set',
'87':'NTFS volume set',
'88':'Linux plaintext',
'8e':'Linux LVM',
'93':'Amoeba',
'94':'Amoeba BBT',
'9f':'BSD/OS',
'a0':'IBM Thinkpad hi',
'a5':'FreeBSD',
'a6':'OpenBSD',
'a7':'NeXTSTEP',
'a8':'Darwin UFS',
'a9':'NetBSD',
'ab':'Darwin boot',
'af':'HFS / HFS+',
'b7':'BSDI fs',
'b8':'BSDI swap',
'bb':'Boot Wizard hid',
'be':'Solaris boot',
'bf':'Solaris',
'c1':'DRDOS/sec (FAT-',
'c4':'DRDOS/sec (FAT-',
'c6':'DRDOS/sec (FAT-',
'c7':'Syrinx',
'da':'Non-FS data',
'db':'CP/M / CTOS / .',
'de':'Dell Utility',
'df':'BootIt',
'e1':'DOS access',
'e3':'DOS R/O',
'e4':'SpeedStor',
'eb':'BeOS fs',
'ee':'GPT',
'ef':'EFI (FAT-12/16/',
'f0':'Linux/PA-RISC b',
'f1':'SpeedStor',
'f4':'SpeedStor',
'f2':'DOS secondary',
'fb':'VMware VMFS',
'fc':'VMware VMKCORE',
'fd':'Linux raid auto',
'fe':'LANstep',
'ff':'BBT',
}

mbr_file = open(sys.argv[1], "rb")
mbr_file_read = mbr_file.read(9555555)

mbr_file_raw = binascii.hexlify(mbr_file_read)
mbr_file_string = str(mbr_file_raw)



def beginning_sector_seek(mbr_drive, which_partition):
    if which_partition == 1:
        for i in range(0, len(mbr_drive)):
            if i != 918:
                i + 918
            elif i == 918:
                current_sector = mbr_drive[i-8:i]
                return current_sector

    if which_partition == 2:
        for i in range(0, len(mbr_drive)):
            if i != 950:
                i + 950
            elif i == 950:
                current_sector = mbr_drive[i-8:i]
                return current_sector

    if which_partition == 3:
        for i in range(0, len(mbr_drive)):
            if i != 982:
                i + 982
            elif i == 982:
                current_sector = mbr_drive[i-8:i]
                return current_sector

    if which_partition == 4:
        for i in range(0, len(mbr_drive)):
            if i != 1014:
                i + 1014
            elif i == 1014:
                current_sector = mbr_drive[i-8:i]
                return current_sector
        if current_sector == '00000000':
            return 0
        else:
            return current_sector

starting_sector_hex_1 = beginning_sector_seek(mbr_file_string, 1)
starting_sector_hex_2 = beginning_sector_seek(mbr_file_string, 2)
starting_sector_hex_3 = beginning_sector_seek(mbr_file_string, 3)
starting_sector_hex_4 = beginning_sector_seek(mbr_file_string, 4)



def seek_partition_type(mbr_drive, which_partition):
    if which_partition == 1:
        for i in range(0, len(mbr_drive)):
            if i != 918:
                i + 918
            elif i == 918:
                return mbr_drive[i-16:i-14]

    if which_partition == 2:
        for i in range(0, len(mbr_drive)):
            if i != 950:
                i + 950
            elif i == 950:
                return mbr_drive[i-16:i-14]

    if which_partition == 3:
        for i in range(0, len(mbr_drive)):
            if i != 982:
                i + 982
            elif i == 982:
                return mbr_drive[i-16:i-14]

    if which_partition == 4:
        for i in range(0, len(mbr_drive)):
            if i != 1014:
                i + 1014
            elif i == 1014:
                return mbr_drive[i-16:i-14]

partition_1_type = seek_partition_type(mbr_file_string, 1)
partition_2_type = seek_partition_type(mbr_file_string, 2)
partition_3_type = seek_partition_type(mbr_file_string, 3)
partition_4_type = seek_partition_type(mbr_file_string, 4)



def mbr_size_volume(mbr_drive, which_partition):
    if which_partition == 1:  
        for i in range(0, len(mbr_drive)): 
            if i != 1014:
                i + 1014
            elif i == 1014:
                size_of_volume = mbr_drive[i:i+8]
                return size_of_volume

    if which_partition == 2:  
        for i in range(0, len(mbr_drive)): 
            if i != 950:
                i + 950
            elif i == 950:
                size_of_volume= mbr_drive[i:i+8]
                return size_of_volume

    if which_partition == 3:  
        for i in range(0, len(mbr_drive)): 
            if i != 982:
                i + 982
            elif i == 982:
                size_of_volume = mbr_drive[i:i+8]
                return size_of_volume
        
    if which_partition == 4:  
        for i in range(0, len(mbr_drive)): 
            if i != 1014:
                i + 1014
            elif i == 1014:
                size_of_volume = mbr_drive[i:i+8]
                return size_of_volume
        if size_of_volume == '00000000':
            return 0
        else:
            return size_of_volume

sector_1_volume_size = mbr_size_volume(mbr_file_string, 1)
sector_2_volume_size = mbr_size_volume(mbr_file_string, 2)
sector_3_volume_size = mbr_size_volume(mbr_file_string, 3)
sector_4_volume_size = mbr_size_volume(mbr_file_string, 4)



def convert_hex_to_decimal(mbr_drive):
    if mbr_drive == 0:
        return 0
    else:
        format_in_hex = mbr_drive[6] + mbr_drive[7] + mbr_drive[4] + mbr_drive[5] + mbr_drive[2] + mbr_drive[3] + mbr_drive[0] + mbr_drive[1]
        converted_hex = int(format_in_hex, 16)
        return converted_hex

starting_bytes_decimal_1 = convert_hex_to_decimal(starting_sector_hex_1)
starting_bytes_decimal_2 = convert_hex_to_decimal(starting_sector_hex_2)
starting_bytes_decimal_3 = convert_hex_to_decimal(starting_sector_hex_3)
starting_bytes_decimal_4 = convert_hex_to_decimal(starting_sector_hex_4)


def volume_hex_to_decimal(mbr_drive):
    if mbr_drive == 0:
        return 0
    else:
        format_in_hex = mbr_drive[6] + mbr_drive[7] + mbr_drive[4] + mbr_drive[5] + mbr_drive[2] + mbr_drive[3] + mbr_drive[0] + mbr_drive[1]
        converted_volume_hex = int(format_in_hex, 16)
        return converted_volume_hex

volume_bytes_decimal_1 = volume_hex_to_decimal(sector_1_volume_size)
volume_bytes_decimal_2 = volume_hex_to_decimal(sector_2_volume_size)
volume_bytes_decimal_3 = volume_hex_to_decimal(sector_3_volume_size)
volume_bytes_decimal_4 = volume_hex_to_decimal(sector_4_volume_size)


def seek_final_16(mbr_drive, which_partition):
    
    if which_partition == 1:
        for i in range((starting_bytes_decimal_1 * 1024) + 994, (starting_bytes_decimal_1 * 1024) + 1026):
            if i == (starting_bytes_decimal_1 * 1024) + 994:
                return mbr_drive[i:i+32]
    
    if which_partition == 2:
        for i in range((starting_bytes_decimal_2 * 1024) + 994, (starting_bytes_decimal_2 * 1024) + 1026):
            if i == (starting_bytes_decimal_2 * 1024) + 994:
                return mbr_drive[i:i+32]
   
    if which_partition == 3:
        for i in range((starting_bytes_decimal_3 * 1024) + 994, (starting_bytes_decimal_3 * 1024) + 1100):
            if i == (starting_bytes_decimal_3 * 1024) + 994:
                return mbr_drive[i:i+32]
    
    if which_partition == 4:
        for i in range((starting_bytes_decimal_4 * 1024) + 994, (starting_bytes_decimal_4 * 1024) + 1026):
            if i == (starting_bytes_decimal_4 * 1024) + 994:
                return mbr_drive[i:i+32]

final_16_partition_1 = seek_final_16(mbr_file_string, 1)
final_16_partition_2 = seek_final_16(mbr_file_string, 2)
final_16_partition_3 = seek_final_16(mbr_file_string, 3)
final_16_partition_4 = seek_final_16(mbr_file_string, 4)


def space_final_16(mbr_drive):
    spaced_final_16 = ' '.join(re.findall(r'.{1,2}', mbr_drive))
    return spaced_final_16

final_16_spaced_1 = space_final_16(final_16_partition_1)
final_16_spaced_2 = space_final_16(final_16_partition_2)
final_16_spaced_3 = space_final_16(final_16_partition_3)
final_16_spaced_4 = space_final_16(final_16_partition_4)

print('(' + partition_1_type + ')', partitions[partition_1_type], ',', str(starting_bytes_decimal_1) + ',', volume_bytes_decimal_1 )
print('(' + partition_2_type + ')', partitions[partition_2_type], ',', str(starting_bytes_decimal_2) + ',', volume_bytes_decimal_2 )
print('(' + partition_3_type + ')', partitions[partition_3_type], ',', str(starting_bytes_decimal_3) + ',', volume_bytes_decimal_3 )
print('(' + partition_4_type + ')', partitions[partition_4_type], ',', str(starting_bytes_decimal_4) + ',', volume_bytes_decimal_4 )

print("First Partition: \nLast 16 bytes of partition 1:", final_16_spaced_1)
print("Second Partition: 2 \nLast 16 bytes of partition 2:", final_16_spaced_2)
print("Third Partition: 3 \nLast 16 bytes of partition 3:", final_16_spaced_3)
print("Fourth Partition: 4 \nLast 16 bytes of partition 4:", final_16_spaced_4)