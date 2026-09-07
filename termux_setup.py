#!/usr/bin/env python3
"""
TERMUX SETUP
ELMY0711 EDITION

Menu:
1. Basic
2. Python Dev
3. Web Dev
4. Go Dev
5. Security / Network
6. Full Package
0. Exit

Run:
    python3 termux_setup.py
"""

import os
import shutil
import subprocess
import sys
import time


# ============================================================
# COLORS
# ============================================================

R = "\033[0m"
B = "\033[1m"
D = "\033[2m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
WHITE = "\033[97m"


# ============================================================
# PACKAGE LIST
# ============================================================

PACKAGES = {

    # --------------------------------------------------------
    # 1. BASIC
    # --------------------------------------------------------

    "basic": [
        "bash",
        "coreutils",
        "findutils",
        "grep",
        "sed",
        "gawk",
        "tar",
        "gzip",
        "bzip2",
        "xz-utils",
        "unzip",
        "zip",
        "file",
        "which",
        "procps",
        "util-linux",
        "nano",
        "vim",
        "less",
        "tree",
        "htop",
        "tmux",
        "fish",
        "man",
    ],

    # --------------------------------------------------------
    # 2. PYTHON DEV
    # --------------------------------------------------------

    "python": [
        "python",
        "python-pip",
        "clang",
        "make",
        "pkg-config",
        "libffi",
        "openssl",
        "rust",
        "git",
    ],

    # --------------------------------------------------------
    # 3. WEB DEV
    # --------------------------------------------------------

    "web": [
        "git",
        "curl",
        "wget",
        "openssl",
        "nodejs",
        "npm",
        "php",
        "python",
        "python-pip",
        "sqlite",
    ],

    # --------------------------------------------------------
    # 4. GO DEV
    # --------------------------------------------------------

    "go": [
        "golang",
        "git",
        "clang",
        "make",
        "cmake",
        "pkg-config",
        "curl",
        "wget",
    ],

    # --------------------------------------------------------
    # 5. SECURITY / NETWORK
    # --------------------------------------------------------

    "security": [
        "curl",
        "wget",
        "openssl",
        "openssh",
        "dnsutils",
        "inetutils",
        "net-tools",
        "iproute2",
        "nmap",
        "whois",
        "git",
        "jq",
        "tcpdump",
    ],
}


# ============================================================
# UI
# ============================================================

def clear():
    os.system("clear")


def banner():
    print(CYAN + B)
    print("╭──────────────────────────────────────╮")
    print("│          TERMUX SETUP                │")
    print("│          ELMY0711 EDITION            │")
    print("╰──────────────────────────────────────╯")
    print(R)


def title(text):
    print()
    print(CYAN + B + f"╭─[ {text} ]" + R)


def ok(text):
    print(GREEN + "  ✓ " + R + text)


def warn(text):
    print(YELLOW + "  ! " + R + text)


def error(text):
    print(RED + "  ✗ " + R + text)


def info(text):
    print(CYAN + "  → " + R + text)


def pause():
    print()
    input(D + "ENTER untuk kembali..." + R)


# ============================================================
# COMMAND
# ============================================================

def command_exists(command):
    return shutil.which(command) is not None


def run(command, quiet=True):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None,
            check=False,
        )
        return result.returncode == 0

    except KeyboardInterrupt:
        print()
        warn("Proses dihentikan.")
        return False

    except Exception:
        return False


# ============================================================
# TERMUX CHECK
# ============================================================

def check_termux():
    if not os.environ.get("PREFIX"):
        error("Environment Termux tidak ditemukan.")
        sys.exit(1)

    if not command_exists("pkg"):
        error("Command 'pkg' tidak ditemukan.")
        sys.exit(1)


# ============================================================
# REPOSITORY
# ============================================================

def update_repo():
    title("Repository")

    info("Updating package list...")

    if run(["pkg", "update", "-y"], quiet=False):
        ok("Repository updated")
    else:
        warn("pkg update gagal")


def upgrade_repo():
    info("Checking package upgrade...")

    if run(["pkg", "upgrade", "-y"], quiet=False):
        ok("Package upgrade selesai")
    else:
        warn("pkg upgrade gagal")


# ============================================================
# INSTALL PACKAGE
# ============================================================

def install_package(package):
    info(f"Install {package} ...")

    if command_exists(package):
        ok(f"{package} sudah tersedia")
        return True

    if run(["pkg", "install", "-y", package]):
        ok(f"{package} installed")
        return True

    error(f"{package} gagal diinstall")
    return False


def install_packages(packages):
    success = 0
    failed = 0

    total = len(packages)

    print()

    for index, package in enumerate(packages, 1):

        print(
            D +
            f"[{index}/{total}] " +
            R,
            end=""
        )

        if install_package(package):
            success += 1
        else:
            failed += 1

    print()
    print(
        GREEN +
        f"  ✓ Berhasil : {success}" +
        R
    )

    if failed:
        print(
            YELLOW +
            f"  ! Gagal    : {failed}" +
            R
        )


# ============================================================
# DIRECTORY SETUP
# ============================================================

def setup_directories():
    title("Directories")

    home = os.path.expanduser("~")

    folders = [
        "bin",
        "tools",
        "scripts",
        "projects",
        "downloads",
    ]

    for folder in folders:
        path = os.path.join(home, folder)

        try:
            os.makedirs(path, exist_ok=True)
            ok(f"~/{folder}")

        except Exception as e:
            error(f"~/ {folder}")


# ============================================================
# STORAGE
# ============================================================

def setup_storage():
    title("Storage")

    if command_exists("termux-setup-storage"):
        info("Request storage permission...")
        run(["termux-setup-storage"], quiet=False)
        ok("Storage setup selesai")
    else:
        warn("termux-api/storage command tidak tersedia")


# ============================================================
# PYTHON SETUP
# ============================================================

def python_setup():
    title("Python")

    if not command_exists("python"):
        warn("Python tidak tersedia.")
        return

    ok("Python tersedia")

    info("Upgrade pip...")

    if run(
        [
            "python",
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ]
    ):
        ok("pip updated")
    else:
        warn("pip upgrade gagal")


# ============================================================
# GO SETUP
# ============================================================

def go_setup():
    title("Go")

    if not command_exists("go"):
        warn("Go tidak tersedia.")
        return

    try:
        result = subprocess.run(
            ["go", "version"],
            capture_output=True,
            text=True,
            check=False,
        )

        version = (
            result.stdout.strip()
            or result.stderr.strip()
        )

        ok(version)

    except Exception:
        warn("Tidak dapat membaca versi Go")


# ============================================================
# WEB SETUP
# ============================================================

def web_setup():
    title("Web Development")

    if command_exists("node"):
        run(["node", "--version"], quiet=False)
    else:
        warn("Node.js tidak tersedia")

    if command_exists("npm"):
        run(["npm", "--version"], quiet=False)
    else:
        warn("NPM tidak tersedia")

    if command_exists("php"):
        run(["php", "--version"], quiet=False)
    else:
        warn("PHP tidak tersedia")


# ============================================================
# VERSION CHECK
# ============================================================

def versions():
    title("Installed Tools")

    tools = [
        ("Python", "python", "--version"),
        ("Git", "git", "--version"),
        ("Node", "node", "--version"),
        ("NPM", "npm", "--version"),
        ("Go", "go", "version"),
        ("PHP", "php", "--version"),
        ("Clang", "clang", "--version"),
        ("Curl", "curl", "--version"),
        ("Wget", "wget", "--version"),
        ("Nmap", "nmap", "--version"),
        ("Fish", "fish", "--version"),
        ("Tmux", "tmux", "-V"),
    ]

    for name, command, argument in tools:

        if not command_exists(command):
            continue

        try:
            result = subprocess.run(
                [command, argument],
                capture_output=True,
                text=True,
                check=False,
            )

            output = (
                result.stdout.strip()
                or result.stderr.strip()
            )

            first = (
                output.splitlines()[0]
                if output
                else "OK"
            )

            print(
                f"  {GREEN}✓{R} "
                f"{name:<8} "
                f"{D}{first}{R}"
            )

        except Exception:
            pass


# ============================================================
# INSTALL FLOW
# ============================================================

def install_profile(name, label):

    title(label)

    packages = PACKAGES[name]

    print(
        f"  Package: {B}{len(packages)}{R}"
    )

    print()

    answer = input(
        "  Lanjut install? [Y/n]: "
    ).strip().lower()

    if answer not in ("", "y", "yes"):
        warn("Dibatalkan.")
        return

    update_repo()
    install_packages(packages)

    if name == "python":
        python_setup()

    elif name == "go":
        go_setup()

    elif name == "web":
        web_setup()

    versions()

    pause()


# ============================================================
# FULL PACKAGE
# ============================================================

def full_package():

    title("FULL PACKAGE")

    all_packages = []

    for packages in PACKAGES.values():
        all_packages.extend(packages)

    # Remove duplicate packages
    all_packages = list(dict.fromkeys(all_packages))

    print(
        f"  Total package unik: "
        f"{B}{len(all_packages)}{R}"
    )

    print()
    warn("Mode Full Package bisa membutuhkan banyak")
    warn("storage dan waktu instalasi.")

    print()

    answer = input(
        "  Lanjut? [Y/n]: "
    ).strip().lower()

    if answer not in ("", "y", "yes"):
        warn("Dibatalkan.")
        return

    update_repo()
    upgrade_repo()

    setup_directories()
    setup_storage()

    install_packages(all_packages)

    python_setup()
    go_setup()
    web_setup()

    versions()

    pause()


# ============================================================
# MENU
# ============================================================

def menu():

    while True:

        clear()
        banner()

        print("  " + B + "MENU UTAMA" + R)
        print()
        print("  " + CYAN + "1" + R + ". Basic")
        print("  " + CYAN + "2" + R + ". Python Dev")
        print("  " + CYAN + "3" + R + ". Web Dev")
        print("  " + CYAN + "4" + R + ". Go Dev")
        print("  " + CYAN + "5" + R + ". Security / Network")
        print("  " + CYAN + "6" + R + ". Full Package")
        print("  " + RED + "0" + R + ". Exit")
        print()

        try:
            choice = input(
                "  Pilih [0-6]: "
            ).strip().lower()

        except KeyboardInterrupt:
            print()
            return

        if choice == "1":
            install_profile(
                "basic",
                "BASIC"
            )

        elif choice == "2":
            install_profile(
                "python",
                "PYTHON DEVELOPMENT"
            )

        elif choice == "3":
            install_profile(
                "web",
                "WEB DEVELOPMENT"
            )

        elif choice == "4":
            install_profile(
                "go",
                "GO DEVELOPMENT"
            )

        elif choice == "5":
            install_profile(
                "security",
                "SECURITY / NETWORK"
            )

        elif choice == "6":
            full_package()

        elif choice in ("0", "q", "quit", "exit"):
            clear()
            print()
            print(
                GREEN +
                "  ✓ Termux Setup selesai. Bye!" +
                R
            )
            print()
            return

        else:
            warn("Pilihan tidak valid.")
            time.sleep(1)


# ============================================================
# MAIN
# ============================================================

def main():

    clear()

    try:
        check_termux()
        setup_directories()
        menu()

    except KeyboardInterrupt:
        print()
        print(
            YELLOW +
            "\n  ! Program dihentikan." +
            R
        )


if __name__ == "__main__":
    main()
