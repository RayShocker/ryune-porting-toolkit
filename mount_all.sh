#!/bin/bash
M=~/port/mnt
ro() { mkdir -p "$2"; mountpoint -q "$2" || sudo mount -o loop,ro "$1" "$2"; }
ro ~/port/s20/super/system.img  $M/system
ro ~/port/s20/super/vendor.img  $M/vendor
ro ~/port/s20/super/product.img $M/product
ro ~/port/s20/super/odm.img     $M/odm
ro ~/port/s10/system.img        $M/s10system
ro ~/port/s10/vendor.img        $M/s10vendor
ro ~/port/s10/csc/product.img   $M/s10product
mkdir -p $M/new_system
mountpoint -q $M/new_system || sudo mount -o loop ~/port/build/system_new.img $M/new_system
df -h $M/system $M/vendor $M/product $M/odm $M/s10system $M/s10vendor $M/s10product $M/new_system
