#!/usr/bin/env python3
"""
╭──────────────────────────────────────────────╮
│              TERMUX SETUP v2.0              │
│                 PRO EDITION                 │
│                  ELMY0711                   │
╰──────────────────────────────────────────────╯

Menu:
  1. Basic
  2. Python Dev
  3. Web Dev
  4. Go Dev
  5. Security / Network
  6. Full Package
  7. Shell & Fish
  8. Git Setup
  9. System Tools
 10. Check Installation
  0. Exit

Features:
  - Batch package installation
  - Dependency detection
  - Retry failed installation
  - Installation log
  - Backup config
  - Storage detection
  - Python venv setup
  - Git setup
  - Fish setup
  - Architecture detection
  - Termux environment detection
  - Final installation summary
  - Safe to run repeatedly
"""

import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime


# ============================================================
# CONFIG
# ============================================================

VERSION = "2.0"

HOME = Path.home()
PREFIX = Path(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"))

LOG_FILE = HOME / "termux-setup.log"
BACKUP_DIR = HOME / "termux-backup"
VENV_DIR = HOME / "venvs"
PROJECT_DIR = HOME / "projects"
TOOLS_DIR = HOME / "tools"
SCRIPT_DIR = HOME / "scripts"
BIN_DIR = HOME / "bin"

# ============================================================
# COLORS
# ============================================================

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
WHITE = "\033[97m"
MAGENTA = "\033[35m"


# ============================================================
# STATISTICS
# ============================================================

stats = {
    "installed": 0,
    "already": 0,
    "failed": 0,
    "skipped": 0,
}


# ============================================================
# PACKAGE PROFILES
# ============================================================

PACKAGES = {

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
    ],

    "python": [
        "python",
        "python-pip",
        "git",
        "clang",
        "make",
        "pkg-config",
        "libffi",
        "openssl",
        "rust",
    ],

    "web": [
        "git",
        "curl",
        "wget",
        "openssl",
        "python",
        "python-pip",
        "nodejs",
        "npm",
        "php",
        "sqlite",
    ],

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
        "jq",
        "tcpdump",
        "git",
    ],

    "shell": [
        "bash",
        "fish",
        "tmux",
        "nano",
        "vim",
        "less",
        "tree",
    ],

    "git": [
        "git",
        "openssh",
        "curl",
    ],

    "system": [
        "coreutils",
        "procps",
        "util-linux",
        "psmisc",
        "htop",
        "lsof",
        "file",
        "which",
        "jq",
        "rsync",
        "sqlite",
    ],
}


# ============================================================
# UI
# ============================================================

def clear():
    os.system("clear")


def banner():
    print(CYAN + BOLD)
    print("╭──────────────────────────────────────╮")
    print("│          TERMUX SETUP v2.0           │")
    print("│             PRO EDITION              │")
    print("│              ELMY0711                │")
    print("╰──────────────────────────────────────╯")
    print(RESET)


def section(text):
    print()
    print(CYAN + BOLD + f"╭─[ {text} ]" + RESET)


def line():
    print(DIM + "─" * 40 + RESET)


def ok(text):
    print(GREEN + "  ✓ " + RESET + text)


def warn(text):
    print(YELLOW + "  ! " + RESET + text)


def error(text):
    print(RED + "  ✗ " + RESET + text)


def info(text):
    print(CYAN + "  → " + RESET + text)


def log(text):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")

    except Exception:
        pass


def pause():
    print()
    try:
        input(DIM + "ENTER untuk kembali..." + RESET)
    except KeyboardInterrupt:
        pass


# ============================================================
# COMMAND HELPERS
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

    except Exception as exc:
        log(f"COMMAND ERROR: {command} -> {exc}")
        return False


def command_output(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        return (
            result.stdout.strip()
            or result.stderr.strip()
        )

    except Exception:
        return ""


# ============================================================
# TERMUX CHECK
# ============================================================

def check_termux():
    section("Environment")

    if not os.environ.get("PREFIX"):
        error("PREFIX tidak ditemukan.")
        error("Script ini dirancang untuk Termux.")
        return False

    if not command_exists("pkg"):
        error("Command pkg tidak ditemukan.")
        return False

    ok("Termux detected")
    ok(f"PREFIX : {PREFIX}")
    ok(f"HOME   : {HOME}")

    arch = platform.machine()

    if arch:
        ok(f"Arch   : {arch}")

    return True


# ============================================================
# DIRECTORY SETUP
# ============================================================

def setup_directories():
    section("Directory Setup")

    directories = [
        BIN_DIR,
        TOOLS_DIR,
        SCRIPT_DIR,
        PROJECT_DIR,
        VENV_DIR,
        BACKUP_DIR,
    ]

    for directory in directories:

        try:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            ok(str(directory))

        except Exception as exc:
            error(f"{directory}: {exc}")


# ============================================================
# STORAGE
# ============================================================

def setup_storage():
    section("Storage")

    storage = HOME / "storage"

    if storage.exists():
        ok("~/storage tersedia")
        return

    if command_exists("termux-setup-storage"):

        info("Meminta permission storage...")

        run(
            ["termux-setup-storage"],
            quiet=False,
        )

        if storage.exists():
            ok("Storage aktif")
        else:
            warn(
                "Permission mungkin belum diberikan."
            )

    else:
        warn(
            "termux-setup-storage tidak ditemukan."
        )


# ============================================================
# REPOSITORY
# ============================================================

def update_repository():

    section("Repository")

    info("Updating package list...")

    log("Running pkg update")

    if run(
        ["pkg", "update", "-y"],
        quiet=False,
    ):
        ok("Repository updated")
        return True

    error("pkg update gagal")
    return False


def upgrade_repository():

    info("Checking package upgrade...")

    log("Running pkg upgrade")

    if run(
        ["pkg", "upgrade", "-y"],
        quiet=False,
    ):
        ok("Package upgrade selesai")
        return True

    warn("pkg upgrade gagal")
    return False


# ============================================================
# PACKAGE STATUS
# ============================================================

def package_installed(package):
    """
    pkg list-installed output can vary between versions.
    dpkg-query is used when available.
    """

    if command_exists("dpkg-query"):

        result = subprocess.run(
            [
                "dpkg-query",
                "-W",
                "-f=${Status}",
                package,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        return "install ok installed" in result.stdout

    return False


def package_available(package):
    """
    Check package availability using apt-cache.
    If the command is unavailable, assume available
    and let pkg handle it.
    """

    if not command_exists("apt-cache"):
        return True

    result = subprocess.run(
        [
            "apt-cache",
            "show",
            package,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )

    return result.returncode == 0


# ============================================================
# BATCH INSTALLER
# ============================================================

def install_packages(packages):

    packages = list(dict.fromkeys(packages))

    if not packages:
        return

    section("Package Installation")

    total = len(packages)

    pending = []
    unavailable = []

    for package in packages:

        if package_installed(package):
            stats["already"] += 1
            ok(f"{package} sudah terinstall")
            continue

        if not package_available(package):
            unavailable.append(package)
            stats["skipped"] += 1
            warn(f"{package} tidak tersedia")
            continue

        pending.append(package)

    if unavailable:
        log(
            "Unavailable: " +
            ", ".join(unavailable)
        )

    if not pending:
        ok("Semua package sudah tersedia.")
        return

    print()

    info(
        f"Installing {len(pending)} package "
        f"dalam satu batch..."
    )

    log(
        "Installing: " +
        ", ".join(pending)
    )

    command = [
        "pkg",
        "install",
        "-y",
    ] + pending

    if run(command, quiet=False):

        stats["installed"] += len(pending)

        print()

        for package in pending:
            ok(package)

        log("Batch installation success")
        return

    # --------------------------------------------------------
    # RETRY INDIVIDUAL
    # --------------------------------------------------------

    warn(
        "Batch install gagal."
    )

    warn(
        "Mencoba package satu per satu..."
    )

    for package in pending:

        info(f"Retry: {package}")

        if run(
            ["pkg", "install", "-y", package],
            quiet=False,
        ):
            stats["installed"] += 1
            ok(package)
            log(f"SUCCESS: {package}")

        else:
            stats["failed"] += 1
            error(package)
            log(f"FAILED: {package}")


# ============================================================
# PYTHON
# ============================================================

def python_setup():

    section("Python Development")

    if not command_exists("python"):
        warn("Python belum tersedia.")
        return

    version = command_output(
        ["python", "--version"]
    )

    ok(version or "Python tersedia")

    if command_exists("pip"):

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

    # --------------------------------------------------------
    # VENV
    # --------------------------------------------------------

    VENV_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    venv = VENV_DIR / "default"

    if not venv.exists():

        info("Membuat Python virtual environment...")

        if run(
            [
                "python",
                "-m",
                "venv",
                str(venv),
            ]
        ):
            ok(f"venv dibuat: {venv}")

        else:
            warn(
                "venv gagal dibuat."
            )

    else:
        ok(f"venv tersedia: {venv}")


# ============================================================
# GO
# ============================================================

def go_setup():

    section("Go Development")

    if not command_exists("go"):
        warn("Go belum tersedia.")
        return

    version = command_output(
        ["go", "version"]
    )

    ok(version or "Go tersedia")

    gopath = HOME / "go"

    try:
        (gopath / "bin").mkdir(
            parents=True,
            exist_ok=True,
        )

        (gopath / "src").mkdir(
            parents=True,
            exist_ok=True,
        )

        ok(f"GOPATH directory: {gopath}")

    except Exception:
        warn("GOPATH directory gagal dibuat")


# ============================================================
# WEB
# ============================================================

def web_setup():

    section("Web Development")

    tools = [
        ("Node.js", "node", ["node", "--version"]),
        ("NPM", "npm", ["npm", "--version"]),
        ("PHP", "php", ["php", "--version"]),
        ("Python", "python", ["python", "--version"]),
    ]

    for name, command, version_cmd in tools:

        if not command_exists(command):
            warn(f"{name}: tidak tersedia")
            continue

        output = command_output(version_cmd)

        if output:
            ok(f"{name}: {output.splitlines()[0]}")
        else:
            ok(f"{name}: tersedia")


# ============================================================
# FISH
# ============================================================

def fish_setup():

    section("Fish Shell")

    if not command_exists("fish"):
        warn("Fish belum tersedia.")
        return

    fish_config = HOME / ".config" / "fish"

    try:
        fish_config.mkdir(
            parents=True,
            exist_ok=True,
        )

        ok(
            f"Fish config: {fish_config}"
        )

    except Exception:
        warn("Gagal membuat Fish config.")

    fish_path = command_output(
        ["which", "fish"]
    )

    if fish_path:
        ok(f"Fish binary: {fish_path}")


# ============================================================
# GIT
# ============================================================

def git_setup():

    section("Git Setup")

    if not command_exists("git"):
        warn("Git belum tersedia.")
        return

    version = command_output(
        ["git", "--version"]
    )

    ok(version or "Git tersedia")

    print()

    try:
        name = input(
            "  Git username "
            "(ENTER = skip): "
        ).strip()

        email = input(
            "  Git email "
            "(ENTER = skip): "
        ).strip()

    except KeyboardInterrupt:
        print()
        warn("Git setup dibatalkan.")
        return

    if name:

        run(
            [
                "git",
                "config",
                "--global",
                "user.name",
                name,
            ]
        )

        ok("Git username disimpan")

    if email:

        run(
            [
                "git",
                "config",
                "--global",
                "user.email",
                email,
            ]
        )

        ok("Git email disimpan")

    run(
        [
            "git",
            "config",
            "--global",
            "init.defaultBranch",
            "main",
        ]
    )

    ok("Default branch: main")


# ============================================================
# BACKUP
# ============================================================

def backup_configs():

    section("Config Backup")

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    configs = [
        HOME / ".bashrc",
        HOME / ".profile",
        HOME / ".termux",
        HOME / ".config" / "fish",
        HOME / ".gitconfig",
    ]

    found = 0

    for source in configs:

        if not source.exists():
            continue

        try:

            destination = (
                BACKUP_DIR /
                source.name
            )

            if source.is_dir():

                destination = (
                    BACKUP_DIR /
                    f"{source.name}-backup"
                )

                if destination.exists():
                    shutil.rmtree(
                        destination
                    )

                shutil.copytree(
                    source,
                    destination,
                )

            else:

                shutil.copy2(
                    source,
                    destination,
                )

            ok(f"Backup: {source}")
            found += 1

        except Exception as exc:
            warn(
                f"Backup gagal: "
                f"{source}"
            )
            log(
                f"Backup error: {exc}"
            )

    if found == 0:
        info("Tidak ada config yang perlu dibackup.")

    else:
        ok(
            f"{found} config berhasil dibackup."
        )


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def system_info():

    section("System Information")

    values = [
        (
            "Architecture",
            platform.machine()
        ),
        (
            "OS",
            platform.system()
        ),
        (
            "Python",
            platform.python_version()
        ),
        (
            "Termux PREFIX",
            str(PREFIX)
        ),
    ]

    for name, value in values:
        print(
            f"  {WHITE}{name:<18}{RESET}"
            f"{DIM}{value}{RESET}"
        )

    if command_exists("termux-info"):

        print()

        info("Termux information:")

        output = command_output(
            ["termux-info"]
        )

        if output:

            for line_text in output.splitlines():
                print(
                    "    " +
                    DIM +
                    line_text +
                    RESET
                )


# ============================================================
# VERSION CHECK
# ============================================================

def check_tools():

    section("Installation Check")

    tools = [
        ("Python", "python", ["python", "--version"]),
        ("Pip", "pip", ["pip", "--version"]),
        ("Git", "git", ["git", "--version"]),
        ("Curl", "curl", ["curl", "--version"]),
        ("Wget", "wget", ["wget", "--version"]),
        ("Node", "node", ["node", "--version"]),
        ("NPM", "npm", ["npm", "--version"]),
        ("Go", "go", ["go", "version"]),
        ("PHP", "php", ["php", "--version"]),
        ("Clang", "clang", ["clang", "--version"]),
        ("Fish", "fish", ["fish", "--version"]),
        ("Tmux", "tmux", ["tmux", "-V"]),
        ("Nmap", "nmap", ["nmap", "--version"]),
        ("SSH", "ssh", ["ssh", "-V"]),
        ("SQLite", "sqlite3", ["sqlite3", "--version"]),
        ("JQ", "jq", ["jq", "--version"]),
    ]

    available = 0
    missing = 0

    for name, command, version_cmd in tools:

        if not command_exists(command):

            print(
                f"  {RED}✗{RESET} "
                f"{name:<10} "
                f"{DIM}missing{RESET}"
            )

            missing += 1
            continue

        output = command_output(
            version_cmd
        )

        first = (
            output.splitlines()[0]
            if output
            else "available"
        )

        print(
            f"  {GREEN}✓{RESET} "
            f"{name:<10} "
            f"{DIM}{first}{RESET}"
        )

        available += 1

    print()

    ok(f"Available : {available}")
    warn(f"Missing   : {missing}")


# ============================================================
# PROFILE INSTALL
# ============================================================

def install_profile(key, name):

    clear()
    banner()

    section(name)

    packages = list(
        dict.fromkeys(
            PACKAGES[key]
        )
    )

    print(
        f"  Package: "
        f"{BOLD}{len(packages)}{RESET}"
    )

    print()

    answer = input(
        "  Install profile ini? [Y/n]: "
    ).strip().lower()

    if answer not in ("", "y", "yes"):
        warn("Dibatalkan.")
        time.sleep(1)
        return

    backup_configs()

    update_repository()

    install_packages(packages)

    if key == "python":
        python_setup()

    elif key == "web":
        web_setup()

    elif key == "go":
        go_setup()

    elif key == "shell":
        fish_setup()

    elif key == "git":
        git_setup()

    check_tools()

    pause()


# ============================================================
# FULL PACKAGE
# ============================================================

def full_package():

    clear()
    banner()

    section("FULL PACKAGE")

    packages = []

    for group in PACKAGES.values():
        packages.extend(group)

    packages = list(
        dict.fromkeys(packages)
    )

    print(
        f"  Unique package: "
        f"{BOLD}{len(packages)}{RESET}"
    )

    print()

    warn(
        "Full Package dapat membutuhkan"
    )
    warn(
        "storage dan waktu instalasi lebih besar."
    )

    print()

    answer = input(
        "  Lanjutkan? [Y/n]: "
    ).strip().lower()

    if answer not in ("", "y", "yes"):
        warn("Dibatalkan.")
        time.sleep(1)
        return

    backup_configs()

    update_repository()
    upgrade_repository()

    setup_directories()
    setup_storage()

    install_packages(packages)

    python_setup()
    go_setup()
    web_setup()
    fish_setup()

    check_tools()

    pause()


# ============================================================
# SYSTEM TOOLS MENU
# ============================================================

def system_tools():

    clear()
    banner()

    section("SYSTEM TOOLS")

    setup_directories()
    setup_storage()

    system_info()

    check_tools()

    pause()


# ============================================================
# SHELL MENU
# ============================================================

def shell_menu():

    clear()
    banner()

    section("SHELL & FISH")

    backup_configs()

    install_packages(
        PACKAGES["shell"]
    )

    fish_setup()

    print()

    warn(
        "Config shell tidak diubah otomatis."
    )

    warn(
        "config.fish user tetap aman."
    )

    pause()


# ============================================================
# MAIN MENU
# ============================================================

def menu():

    while True:

        clear()
        banner()

        print("  " + BOLD + "MENU UTAMA" + RESET)
        print()

        print(
            "  " + CYAN + "1" + RESET +
            ". Basic"
        )

        print(
            "  " + CYAN + "2" + RESET +
            ". Python Dev"
        )

        print(
            "  " + CYAN + "3" + RESET +
            ". Web Dev"
        )

        print(
            "  " + CYAN + "4" + RESET +
            ". Go Dev"
        )

        print(
            "  " + CYAN + "5" + RESET +
            ". Security / Network"
        )

        print(
            "  " + CYAN + "6" + RESET +
            ". Full Package"
        )

        print(
            "  " + CYAN + "7" + RESET +
            ". Shell & Fish"
        )

        print(
            "  " + CYAN + "8" + RESET +
            ". Git Setup"
        )

        print(
            "  " + CYAN + "9" + RESET +
            ". System Tools"
        )

        print(
            "  " + CYAN + "10" + RESET +
            ". Check Installation"
        )

        print(
            "  " + RED + "0" + RESET +
            ". Exit"
        )

        print()

        try:
            choice = input(
                "  Pilih [0-10]: "
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

        elif choice == "7":

            shell_menu()

        elif choice == "8":

            clear()
            banner()

            backup_configs()
            update_repository()

            install_packages(
                PACKAGES["git"]
            )

            git_setup()

            pause()

        elif choice == "9":

            system_tools()

        elif choice == "10":

            clear()
            banner()

            system_info()
            check_tools()

            pause()

        elif choice in (
            "0",
            "q",
            "quit",
            "exit",
        ):

            clear()

            print()
            print(
                GREEN +
                BOLD +
                "  ✓ Termux Setup selesai." +
                RESET
            )

            print()
            return

        else:

            warn(
                "Pilihan tidak valid."
            )

            time.sleep(1)


# ============================================================
# MAIN
# ============================================================

def main():

    clear()

    if not check_termux():
        print()
        sys.exit(1)

    setup_directories()

    log(
        f"Termux Setup v{VERSION} started"
    )

    try:

        menu()

    except KeyboardInterrupt:

        print()

        warn(
            "Program dihentikan."
        )

        log(
            "Program interrupted"
        )


if __name__ == "__main__":
    main()
