#!/bin/bash
M=~/port/mnt
S10=$M/s10system/system
S20=$M/system/system
O=/mnt/d/Firmware/compare2
mkdir -p $O
{
echo "##### identitas build.prop S10"
sudo grep -E "^ro\.(product|build|system|odm)\.(brand|device|model|name|fingerprint|flavor|characteristics|display|description|first_api|version\.(release|sdk|oneui|incremental|security))" $S10/build.prop
echo "##### identitas build.prop S20"
sudo grep -E "^ro\.(product|build|system|odm)\.(brand|device|model|name|fingerprint|flavor|characteristics|display|description|first_api|version\.(release|sdk|oneui|incremental|security))" $S20/build.prop
echo "##### floating_feature S10 vs S20 (diff)"
sudo diff <(sudo sed 's/[[:space:]]*$//' $S10/etc/floating_feature.xml) <(sudo sed 's/[[:space:]]*$//' $S20/etc/floating_feature.xml)
echo "##### camera-feature S10 vs S20 (diff, 80 baris pertama)"
sudo diff <(sudo sed 's/[[:space:]]*$//' $S10/cameradata/camera-feature.xml) <(sudo sed 's/[[:space:]]*$//' $S20/cameradata/camera-feature.xml) | head -80
echo "##### jumlah berkas"
echo -n "S10: "; sudo find $S10 -type f | wc -l
echo -n "S20: "; sudo find $S20 -type f | wc -l
} > $O/compare2.txt 2>&1
(cd $S10 && sudo find . -type f | sort) > $O/files_s10.txt
(cd $S20 && sudo find . -type f | sort) > $O/files_s20.txt
comm -23 $O/files_s10.txt $O/files_s20.txt > $O/only_s10.txt
comm -13 $O/files_s10.txt $O/files_s20.txt > $O/only_s20.txt
echo "hanya di S10: $(wc -l < $O/only_s10.txt)  hanya di S20: $(wc -l < $O/only_s20.txt)" >> $O/compare2.txt
echo "selesai -> $O"
