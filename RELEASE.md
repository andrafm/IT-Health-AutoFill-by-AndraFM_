# Release Process

## Build Installer

1. Jalankan `build_setup.bat`
2. Tunggu sampai file installer selesai dibuat
3. Hasil utama akan tersedia sebagai `setup.exe`
4. Rename file sesuai versi rilis, misalnya `Setup-IT-Health-AutoFill-1.2.0.exe`

## Publish ke GitHub

1. Commit perubahan source ke branch `main`
2. Push branch `main`
3. Buat tag versi, misalnya `v1.2`
4. Push tag ke GitHub
5. Buat GitHub Release dari tag tersebut
6. Upload asset installer hasil rename versi

## Release Notes Template

```text
IT Health AutoFill vX.Y

Perubahan utama:
- Ringkasan perubahan utama 1.
- Ringkasan perubahan utama 2.
- Ringkasan perubahan utama 3.
```

## Catatan

- Gunakan Inno Setup agar icon installer ikut terbawa.
- GitHub Release dipakai untuk distribusi installer, bukan commit file build ke repo.
- Jika icon tidak berubah di Windows Explorer, refresh icon cache atau rename file installer.
