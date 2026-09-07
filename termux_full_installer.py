#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Termux Full Package Installer
=============================
Script Python untuk menginstal package-package populer di Termux secara otomatis.

Cara penggunaan:
    python termux_full_installer.py

Author: Auto-generated
"""

import subprocess
import sys
import os
import time

# ===================== KONFIGURASI =====================

# Kategori package yang tersedia
PACKAGES = {
    "core": {
        "desc": "Package inti & utilitas dasar",
        "packages": [
            "git", "curl", "wget", "nano", "vim", "htop", "tree",
            "unzip", "zip", "tar", "gzip", "p7zip", "lf", "ncurses-utils",
            "openssh", "termux-api", "termux-tools", "proot", "proot-distro",
            "tsu", "termux-exec", "libandroid-support"
        ]
    },
    "python_dev": {
        "desc": "Python Development",
        "packages": [
            "python", "python-pip", "python-numpy", "python-scipy",
            "python-pillow", "python-lxml", "python-yaml", "python-cryptography",
            "python-bcrypt", "python-paramiko", "python-requests",
            "python-beautifulsoup4", "python-flask", "python-django"
        ]
    },
    "programming": {
        "desc": "Bahasa Pemrograman & Compiler",
        "packages": [
            "clang", "gcc", "make", "cmake", "ninja", "rust", "golang",
            "nodejs", "nodejs-lts", "ruby", "php", "perl", "lua54",
            "lua52", "swift", "kotlin", "openjdk-17", "openjdk-21"
        ]
    },
    "networking": {
        "desc": "Networking & Security Tools",
        "packages": [
            "nmap", "netcat-openbsd", "tcpdump", "wireshark-gtk", "masscan",
            "hydra", "sqlmap", "metasploit", "aircrack-ng", "bettercap",
            "proxychains-ng", "tor", "torsocks", "openssl-tool", "whois",
            "dnsutils", "inetutils", "iproute2", "iw"
        ]
    },
    "web_dev": {
        "desc": "Web Development & Database",
        "packages": [
            "nginx", "apache2", "mariadb", "postgresql", "redis", "sqlite",
            "php-apache", "php-fpm", "phpmyadmin", "composer", "npm", "yarn"
        ]
    },
    "media": {
        "desc": "Media Processing",
        "packages": [
            "ffmpeg", "imagemagick", "sox", "mpg123", "mpv", "cmus",
            "libcaca", "figlet", "cowsay", "lolcat", "neofetch", "screenfetch"
        ]
    },
    "hacking": {
        "desc": "Penetration Testing & Hacking",
        "packages": [
            "nmap", "nikto", "dirb", "gobuster", "wfuzz", "burpsuite",
            "john", "hashcat", "binwalk", "exiftool", "steghide",
            "radare2", "gdb", "strace", "ltrace"
        ]
    },
    "misc": {
        "desc": "Miscellaneous & Fun",
        "packages": [
            "sl", "cmatrix", "asciiquarium", "pipes-sh", "nyancat",
            "fortune", "cowsay", "figlet", "toilet", "boxes"
        ]
    }
}

# Package yang butuh repo tambahan
EXTRA_REPOS = [
    "root-repo",
    "x11-repo",
    "unstable-repo"
]

# ===================== FUNGSI UTILITAS =====================

def print_banner():
    """Menampilkan banner aplikasi."""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║           TERMUX FULL PACKAGE INSTALLER v2.0                 ║
║     Instalasi otomatis package Termux dengan Python          ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_command(cmd, description=""):
    """Menjalankan perintah shell dan menampilkan output."""
    if description:
        print(f"\n[⏳] {description}")
    print(f"[CMD] {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[❌] Error: {e}")
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"[❌] Command tidak ditemukan: {cmd[0]}")
        return False

def check_termux():
    """Memastikan script dijalankan di lingkungan Termux."""
    if not os.path.exists("/data/data/com.termux"):
        print("[⚠️]  Peringatan: Script ini didesain untuk Termux!")
        print("[⚠️]  Beberapa package mungkin tidak tersedia di sistem lain.")
        response = input("Lanjutkan anyway? (y/N): ").strip().lower()
        if response not in ('y', 'yes'):
            sys.exit(0)

def update_repos():
    """Update dan upgrade repository Termux."""
    print("\n" + "="*60)
    print("📦 UPDATE & UPGRADE REPOSITORY")
    print("="*60)

    run_command(["pkg", "update", "-y"], "Updating package list...")
    run_command(["pkg", "upgrade", "-y"], "Upgrading installed packages...")
    print("[✅] Repository berhasil di-update!")

def install_extra_repos():
    """Menginstal repository tambahan (root, x11, unstable)."""
    print("\n" + "="*60)
    print("📦 INSTALL REPOSITORY TAMBAHAN")
    print("="*60)

    for repo in EXTRA_REPOS:
        run_command(["pkg", "install", "-y", repo], f"Installing {repo}...")

    # Update lagi setelah tambah repo
    run_command(["pkg", "update", "-y"], "Updating after adding new repos...")
    print("[✅] Repository tambahan berhasil diinstal!")

def install_packages(category, package_list):
    """Menginstal package dari kategori tertentu."""
    print(f"\n{'='*60}")
    print(f"📦 {category.upper()}")
    print(f"{'='*60}")

    failed = []
    success = []
    skipped = []

    total = len(package_list)
    for i, pkg in enumerate(package_list, 1):
        print(f"\n[{i}/{total}] Menginstal: {pkg} ...")

        # Cek apakah package sudah terinstal
        check = subprocess.run(
            ["dpkg", "-s", pkg],
            capture_output=True,
            text=True
        )
        if check.returncode == 0:
            print(f"[⏭️]  {pkg} sudah terinstal, skip.")
            skipped.append(pkg)
            continue

        # Install package
        result = subprocess.run(
            ["pkg", "install", "-y", pkg],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"[✅] {pkg} berhasil diinstal!")
            success.append(pkg)
        else:
            print(f"[❌] {pkg} gagal diinstal!")
            if "Unable to locate package" in result.stderr:
                print(f"   → Package tidak ditemukan di repository.")
            failed.append(pkg)

        time.sleep(0.5)

    # Ringkasan
    print(f"\n📊 Ringkasan {category}:")
    print(f"   ✅ Berhasil: {len(success)}")
    print(f"   ⏭️  Skip (sudah ada): {len(skipped)}")
    print(f"   ❌ Gagal: {len(failed)}")
    if failed:
        print(f"   📋 Gagal: {', '.join(failed)}")

    return success, skipped, failed

def select_categories():
    """Meminta user memilih kategori package yang akan diinstal."""
    print("\n" + "="*60)
    print("📋 PILIH KATEGORI PACKAGE")
    print("="*60)
    print("\nKategori yang tersedia:")

    categories = list(PACKAGES.keys())
    for i, cat in enumerate(categories, 1):
        info = PACKAGES[cat]
        print(f"  {i}. {cat:15s} - {info['desc']} ({len(info['packages'])} pkg)")

    print(f"  A. ALL          - Instal SEMUA kategori")
    print(f"  Q. QUIT         - Keluar")

    while True:
        choice = input("\nPilihan (pisahkan dengan koma, contoh: 1,3,5 atau A): ").strip().upper()

        if choice == 'Q':
            print("👋 Sampai jumpa!")
            sys.exit(0)

        if choice == 'A':
            return categories

        selected = []
        try:
            for c in choice.split(','):
                c = c.strip()
                if c.isdigit():
                    idx = int(c) - 1
                    if 0 <= idx < len(categories):
                        selected.append(categories[idx])
                    else:
                        print(f"[⚠️]  Pilihan {c} tidak valid!")
                else:
                    if c.lower() in categories:
                        selected.append(c.lower())

            if selected:
                return list(dict.fromkeys(selected))  # Remove duplicates
            else:
                print("[⚠️]  Tidak ada pilihan valid!")
        except Exception as e:
            print(f"[⚠️]  Input tidak valid: {e}")

def setup_storage():
    """Setup akses storage Termux."""
    print("\n" + "="*60)
    print("📁 SETUP STORAGE")
    print("="*60)

    if os.path.exists("/data/data/com.termux"):
        response = input("Izinkan Termux mengakses storage internal? (Y/n): ").strip().lower()
        if response in ('', 'y', 'yes'):
            run_command(["termux-setup-storage"], "Setting up storage access...")
            print("[✅] Storage setup selesai!")
        else:
            print("[⏭️]  Skip setup storage.")
    else:
        print("[⏭️]  Skip (bukan lingkungan Termux).")

def setup_pip():
    """Upgrade pip dan install package Python populer."""
    print("\n" + "="*60)
    print("🐍 SETUP PYTHON PIP")
    print("="*60)

    run_command(["pip", "install", "--upgrade", "pip"], "Upgrading pip...")

    pip_packages = [
        "requests", "beautifulsoup4", "lxml", "html5lib",
        "selenium", "scrapy", "pytest", "black", "flake8",
        "pynput", "colorama", "tqdm", "rich", "click",
        "flask", "django", "fastapi", "uvicorn"
    ]

    print(f"\n📦 Menginstal {len(pip_packages)} package Python via pip...")
    for pkg in pip_packages:
        run_command(["pip", "install", "--user", pkg], f"Installing {pkg}")

    print("[✅] Setup pip selesai!")

def generate_report(results):
    """Generate laporan instalasi."""
    print("\n" + "="*60)
    print("📊 LAPORAN INSTALASI")
    print("="*60)

    total_success = 0
    total_failed = 0
    total_skipped = 0

    for cat, (success, skipped, failed) in results.items():
        total_success += len(success)
        total_skipped += len(skipped)
        total_failed += len(failed)

    print(f"""
┌────────────────────────────────────────┐
│  Total Berhasil : {total_success:4d}              │
│  Total Skip      : {total_skipped:4d}              │
│  Total Gagal     : {total_failed:4d}              │
└────────────────────────────────────────┘
    """)

    if total_failed > 0:
        print("📋 Package yang gagal diinstal:")
        for cat, (success, skipped, failed) in results.items():
            if failed:
                print(f"   [{cat}] {', '.join(failed)}")
        print("\n💡 Tips: Package yang gagal mungkin:")
        print("   - Tidak tersedia di repository saat ini")
        print("   - Memerlukan repo tambahan (root/x11)")
        print("   - Memerlukan device yang di-root")

def main():
    """Fungsi utama."""
    print_banner()
    check_termux()

    # Step 1: Update repos
    update_repos()

    # Step 2: Install extra repos
    install_extra_repos()

    # Step 3: Setup storage
    setup_storage()

    # Step 4: Pilih kategori
    selected = select_categories()

    # Step 5: Install package per kategori
    results = {}
    for cat in selected:
        info = PACKAGES[cat]
        results[cat] = install_packages(cat, info["packages"])

    # Step 6: Setup pip
    setup_choice = input("\nSetup Python pip juga? (Y/n): ").strip().lower()
    if setup_choice in ('', 'y', 'yes'):
        setup_pip()

    # Step 7: Laporan
    generate_report(results)

    print("\n" + "="*60)
    print("🎉 INSTALASI SELESAI!")
    print("="*60)
    print("\n💡 Tips penggunaan Termux:")
    print("   • Gunakan 'pkg search <nama>' untuk mencari package")
    print("   • Gunakan 'pkg list-installed' untuk melihat yang terinstal")
    print("   • Gunakan 'termux-change-repo' untuk ganti mirror")
    print("\nSelamat menggunakan Termux! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[⚠️]  Instalasi dibatalkan oleh user.")
        sys.exit(1)
