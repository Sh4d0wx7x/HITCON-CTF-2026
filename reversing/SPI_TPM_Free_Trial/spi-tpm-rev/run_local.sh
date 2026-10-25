#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)/src
flag=${FLAG_PATH:-$root/../flag}
[[ -f $flag ]] || { echo "hitcon{local}" > "$flag"; chmod 400 "$flag"; }

work=$(mktemp -d /tmp/spi-tpm-local.XXXXXX)
trap 'rm -rf "$work"' EXIT

# Build initramfs with the flag
mkdir -p "$work/overlay"
install -m 0400 "$flag" "$work/overlay/flag"
cp "$root/initramfs.cpio.gz" "$work/initramfs.cpio.gz"
( cd "$work/overlay" && find . -print0 | sort -z | cpio --quiet --null -o --format=newc --owner=0:0 ) \
  | gzip -9n >> "$work/initramfs.cpio.gz"

exec "$root/qemu-system-aarch64" \
  -machine virt,gic-version=3 \
  -cpu cortex-a57 \
  -nodefaults -no-reboot \
  -device spi-tpm-dma,id=spi0_dma \
  -device spi-tpm-sram,id=spi0_sram,size=8192 \
  -device stm32h7-spi,id=spi0,dma-backend=spi0_dma,sram-backend=spi0_sram,fifo-size=32 \
  -device "spi-tpm,bus=ssi,firmware-path=$root/libspi_tpm_firmware.so" \
  -display none -serial stdio -nic none \
  -smp 1 -m 64M \
  -kernel "$root/Image" \
  -initrd "$work/initramfs.cpio.gz" \
  -append "console=ttyAMA0,115200 rdinit=/init quiet loglevel=0"
