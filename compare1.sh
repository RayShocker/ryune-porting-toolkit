#!/bin/bash
M=~/port/mnt
echo "##### VENDOR S10 build.prop (vndk/sdk/device)"
sudo grep -E "vndk|ro.vendor.build.version|ro.product.vendor|ro.vendor.build.fingerprint" $M/s10vendor/build.prop
echo "##### VENDOR S20 build.prop"
sudo grep -E "vndk|ro.vendor.build.version|ro.product.vendor|ro.vendor.build.fingerprint" $M/vendor/build.prop
echo "##### S10 vintf (vendor)"
sudo ls $M/s10vendor/etc/vintf
sudo grep -E "target-level|<manifest|<compatibility-matrix" $M/s10vendor/etc/vintf/manifest.xml | head -5
echo "##### S20 vintf (vendor)"
sudo ls $M/vendor/etc/vintf
sudo grep -E "target-level|<manifest|<compatibility-matrix" $M/vendor/etc/vintf/manifest.xml | head -5
echo "##### S10 system root"
sudo ls $M/s10system
echo "##### S10 system/system top-level"
sudo ls $M/s10system/system
echo "##### S10 product / odm dirs inside system?"
sudo ls $M/s10system/system/product 2>&1 | head -20
sudo ls $M/s10system/system/system_ext 2>&1 | head -20
echo "##### sizes"
sudo du -sh $M/s10system/system/app $M/s10system/system/priv-app $M/s10system/system/framework
sudo du -sh $M/s10vendor
echo "##### S10 camera data"
sudo ls $M/s10system/system/cameradata 2>&1
