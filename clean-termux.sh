#!/data/data/com.termux/files/usr/bin/bash

clear

tanya() {
    read -p "$1 [y/N]: " jawab
    [[ $jawab == "y" || $jawab == "Y" ]]
}

menu() {
    clear
    echo "=================================="
    echo " CLEAN TERMUX "
    echo "=================================="
    echo "Ukuran Home Sekarang: $(du -sh ~ 2>/dev/null | awk '{print $1}')"
    echo "=================================="
    echo " [1] Cek 10 Folder Terbesar"
    echo " [2] Hapus Cache Besar Saja"
    echo " [3] Hapus Cache Bahasa"
    echo " [4] Hapus File.deb"
    echo " [5] Hapus Tools DDoS/Benchmark"
    echo " [6] Hapus node_modules"
    echo " [7] Gas Semua Yang Aman"
    echo " [8] Keluar"
    echo "=================================="
    read -p "Pilih menu: " pil
}

while true; do
    menu
    case $pil in
        1) # CEK 10 TERBESAR
            echo ""
            echo "Top 10 Folder Terbesar:"
            du -h --max-depth=1 ~ 2>/dev/null | sort -hr | head -n 10
            read -p "Enter untuk lanjut..."
            ;;

        2) # HAPUS CACHE BESAR - UDAH FIX
            echo ""
            echo "Yang akan dihapus:.termux-themes.cargo.npm.cpan.cache go"
            if tanya "Hapus semua cache? Bisa lega 4GB+"; then
                echo " -> Buka kunci permission dulu..."
                chmod -R u+w ~/go/pkg ~/go/bin ~/.cargo ~/.npm ~/.cpan 2>/dev/null

                echo " -> Hapus cache..."
                rm -rf ~/.termux-themes ~/.cargo ~/.npm ~/.cpan ~/.cache ~/go/pkg ~/go/bin
                echo " -> Selesai dihapus"
            else echo " -> Dilewati"; fi
            read -p "Enter untuk lanjut..."
            ;;

        3) # HAPUS CACHE BAHASA - PAKAI COMMAND RESMI
            echo ""
            if tanya "Jalanin go clean + npm cache clean + pkg autoclean"; then
                echo " -> Bersihin cache Go..."
                go clean -cache -modcache -testcache 2>/dev/null

                echo " -> Bersihin cache NPM..."
                npm cache clean --force 2>/dev/null

                echo " -> Bersihin cache Termux..."
                pkg autoclean -y && pkg clean
                echo " -> Selesai"
            else echo " -> Dilewati"; fi
            read -p "Enter untuk lanjut..."
            ;;

        4) # HAPUS DEB
            if tanya "Hapus semua file.deb di home?"; then
                find ~ -name "*.deb" -delete
                echo " -> Selesai"
            else echo " -> Dilewati"; fi
            read -p "Enter untuk lanjut..."
            ;;

        5) # HAPUS TOOLS
            echo ""
            echo "Target: wrk MikuMikuBeam KARMA-DDoS stress_cf dll"
            if tanya "Hapus folder tool DDoS? Permanen"; then
                rm -rf ~/wrk ~/MikuMikuBeam ~/KARMA-DDoS ~/stress_cf ~/HAQflood ~/HAQFLOODER ~/HAQ_STORM ~/DDoS-Scripts ~/flood ~/flooder ~/OpenDoor
                echo " -> Selesai"
            else echo " -> Dilewati"; fi
            read -p "Enter untuk lanjut..."
            ;;

        6) # HAPUS NODE_MODULES
            if tanya "Hapus folder ~/node_modules?"; then
                chmod -R u+w ~/node_modules 2>/dev/null
                rm -rf ~/node_modules
                echo " -> Selesai"
            else echo " -> Dilewati"; fi
            read -p "Enter untuk lanjut..."
            ;;

        7) # GAS SEMUA AMAN
            echo ""
            echo "Ini akan hapus Step 1,2,3,4 saja. Tools tidak dihapus"
            if tanya "Lanjut hapus semua cache aman?"; then
                echo " -> Buka kunci permission..."
                chmod -R u+w ~/go/pkg ~/go/bin ~/.cargo ~/.npm ~/.cpan ~/node_modules 2>/dev/null

                echo " -> Hapus cache besar..."
                rm -rf ~/.termux-themes ~/.cargo ~/.npm ~/.cpan ~/.cache ~/go/pkg ~/go/bin

                echo " -> Bersihin cache bahasa..."
                go clean -cache -modcache -testcache 2>/dev/null
                npm cache clean --force 2>/dev/null
                pkg autoclean -y && pkg clean

                echo " -> Hapus file.deb..."
                find ~ -name "*.deb" -delete
                echo " -> Semua cache aman sudah dihapus"
            else echo " -> Dibatalkan"; fi
            read -p "Enter untuk lanjut..."
            ;;

        8) # KELUAR
            echo "Ukuran Akhir: $(du -sh ~ 2>/dev/null | awk '{print $1}')"
            echo "Bye~"
            exit 0
            ;;

        *) echo "Menu tidak ada"; sleep 1;;
    esac
done
