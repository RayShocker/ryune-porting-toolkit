# Project RYune: Android ROM Porting Toolkit
A collection of custom scripts (Python and Bash) designed to simplify the Android ROM porting process (especially for Samsung Exynos devices). Created by **RayShocker**.

---

## Scripts and Functions

### 1. `lpunpack.py`
*   **Function:** Replaces the AOSP `lpunpack` tool to extract dynamic partitions from `super.img` without needing to compile the Android source code.
*   **Usage:** 
    ```bash
    python3 lpunpack.py <super.raw.img> <output_folder> [optional_partition_name]
Example: python3 lpunpack.py super.raw.img ~/port/s20/super

###2. `needed.py`
*   **Function:** Detects missing .so libraries. It checks all ELF files in the vendor folder and cross-references them with available libraries in both vendor and system. Highly useful for finding VNDK (Vendor NDK) issues or dependency mismatches during porting.
*   **Usage:**
    ```bash python3 needed.py <vendor_folder> <system_folder> <output_file.txt>
Example: sudo python3 needed.py ~/port/mnt/s10vendor ~/port/mnt/system/system ~/needed.txt

##3. `scan_magic.py`
*    **Function:** Detects compression types or file formats based on magic bytes (hexadecimal codes at the start of a file). Useful for unpacking boot.img or kernel when you don't know if they are compressed with gzip, lz4, xz, cpio, etc.
*    **Usage:**
     ```bash python3 scan_magic.py <file_to_check>
Example: python3 scan_magic.py ~/port/s10/boot_unpacked/kernel

##4. `mount_all.sh`
*    **Function:** Automatically and safely mounts multiple .img files (like system.img, vendor.img, etc.). The script checks if a folder is already mounted to prevent "already mounted" errors.

Note: You need to edit the path variables inside the script first to match your folder structure.

*    **Usage:** 
     ```bash mount_all.sh

##5. `compare1.sh & compare2.sh`
*    **Function:** Compares (diffs) the contents of S10 (Android 12) and S20 (Android 13) ROMs. It extracts important information such as build.prop differences, floating_feature.xml, camera_feature.xml, and generates a list of files exclusive to either device.
*    **Usage:** 
     ```bash compare2.sh (Ensure S10 and S20 partitions are mounted first).
