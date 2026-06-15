#!/bin/bash

# Script Auto Download + Konversi Gambar ke ASCII Art
# Untuk Logo Kepala Elang di Termux

clear

# Warna
merah='\e[31m'
hijau='\e[32m'
kuning='\e[33m'
biru='\e[34m'
ungu='\e[35m'
cyan='\e[36m'
nc='\e[0m'

echo -e "${cyan}════════════════════════════════════════════════════════${nc}"
echo -e "${kuning}       🤖 AUTO ASCII ART GENERATOR - KEPALA ELANG     ${nc}"
echo -e "${cyan}════════════════════════════════════════════════════════${nc}"
echo ""

# Cek dan install dependensi
echo -e "${biru}[✓] Mengecek dependensi...${nc}"

cek_pkg() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${kuning}[!] $1 belum terinstall, menginstall...${nc}"
        pkg install $1 -y
    else
        echo -e "${hijau}[✓] $1 sudah terinstall${nc}"
    fi
}

cek_pkg wget
cek_pkg jp2a
cek_pkg curl

echo ""

# Buat folder untuk gambar
mkdir -p ~/ascii_art
cd ~/ascii_art

echo -e "${biru}════════════════════════════════════════════════════════${nc}"
echo -e "${ungu}Pilih sumber gambar kepala elang:${nc}"
echo -e "${cyan}1) Pixabay (Gambar gratis & legal)${nc}"
echo -e "${cyan}2) Pakai URL sendiri${nc}"
echo -e "${cyan}3) Baca dari file lokal HP${nc}"
echo -e "${biru}════════════════════════════════════════════════════════${nc}"
read -p "Pilihan [1-3]: " pilihan

case $pilihan in
    1)
        echo -e "${kuning}[!] Mendownload gambar kepala elang dari sumber gratis...${nc}"
        # URL gambar elang dari Pixabay (gambar gratis)
        url="https://cdn.pixabay.com/photo/2013/07/18/20/26/eagle-164654_640.jpg"
        wget -O eagle.jpg "$url"
        ;;
    2)
        echo -e "${kuning}[!] Masukkan URL gambar (jpg/png):${nc}"
        read -p "➤ " url
        wget -O eagle.jpg "$url"
        ;;
    3)
        echo -e "${kuning}[!] Pilih gambar dari penyimpanan HP:${nc}"
        echo -e "${cyan}Contoh: /sdcard/Download/elang.jpg${nc}"
        read -p "➤ " file_path
        cp "$file_path" ~/ascii_art/eagle.jpg
        ;;
    *)
        echo -e "${merah}Pilihan salah!${nc}"
        exit 1
        ;;
esac

# Cek apakah gambar berhasil didownload/disalin
if [ ! -f "eagle.jpg" ]; then
    echo -e "${merah}[✗] Gagal mendapatkan gambar!${nc}"
    exit 1
fi

echo -e "${hijau}[✓] Gambar berhasil didapatkan!${nc}"

# Konversi ke ASCII
echo -e "${kuning}[!] Mengkonversi gambar ke ASCII art...${nc}"
echo ""

# Buat ASCII art dengan ukuran 60 karakter lebar
jp2a --colors --width=60 --height=40 eagle.jpg > eagle_ascii.txt

# Tampilkan hasil
echo -e "${hijau}════════════════════════════════════════════════════════${nc}"
echo -e "${ungu}                HASIL ASCII ART KEPALA ELANG             ${nc}"
echo -e "${hijau}════════════════════════════════════════════════════════${nc}"
echo ""
cat eagle_ascii.txt
echo ""

# Simpan ke file untuk digunakan di script stress tester
echo -e "${biru}[✓] ASCII art disimpan di: ~/ascii_art/eagle_ascii.txt${nc}"
echo -e "${biru}[✓] Script logo siap digunakan!${nc}"

# Tanya mau langsung buat script stress tester?
echo ""
echo -e "${kuning}════════════════════════════════════════════════════════${nc}"
echo -e "${cyan}Apakah ingin langsung membuat script stress tester dengan logo ini?${nc}"
echo -e "${cyan}1) Ya, buat script lengkap${nc}"
echo -e "${cyan}2) Tidak, hanya simpan ASCII art saja${nc}"
read -p "Pilihan [1-2]: " buat_script

if [ "$buat_script" == "1" ]; then
    echo -e "${kuning}[!] Membuat script stress tester...${nc}"
    
    # Baca ASCII art ke variable
    ascii_art=$(cat eagle_ascii.txt)
    
    # Buat script lengkap
    cat > ~/stress_final.sh << 'EOF'
#!/bin/bash

# Banner Logo dari ASCII Art yang sudah digenerate
clear
echo -e "\e[33m"
EOF

    # Tambahkan ASCII art ke script
    echo "$ascii_art" >> ~/stress_final.sh
    
    cat >> ~/stress_final.sh << 'EOF'
echo -e "\e[0m"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   WEB STRESS TESTER v3.0                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Warna
merah='\e[31m'
hijau='\e[32m'
kuning='\e[33m'
biru='\e[34m'
cyan='\e[36m'
nc='\e[0m'

echo -e ""
echo -e "${cyan}════════════════════════════════════════════════════════${nc}"
echo -e "${kuning}        STRESS TESTER - UJI KETAHANAN WEBSITE${nc}"
echo -e "${cyan}════════════════════════════════════════════════════════${nc}"
echo -e ""

echo -e "${biru}[?] Masukkan URL target (contoh: https://example.com)${nc}"
read -p "➤ " target

echo -e "${biru}[?] Jumlah request per detik:${nc}"
read -p "➤ " req_detik

echo -e "${biru}[?] Durasi uji (detik):${nc}"
read -p "➤ " durasi

echo -e ""
echo -e "${kuning}╔════════════════════════════════════════════════════════╗${nc}"
echo -e "${kuning}║  🦅  MEMULAI STRESS TEST...                            ║${nc}"
echo -e "${kuning}║  📡  Target: ${target}  ║${nc}"
echo -e "${kuning}║  ⚡  Request/Detik: ${req_detik}  |  Durasi: ${durasi} detik  ║${nc}"
echo -e "${kuning}╚════════════════════════════════════════════════════════╝${nc}"
echo -e "${merah}[!] Tekan CTRL+C untuk berhenti${nc}"
echo ""

total_request=$((req_detik * durasi))
sukses=0
gagal=0

stress_test() {
    local end_time=$((SECONDS + durasi))
    local hitungan=0
    
    while [ $SECONDS -lt $end_time ]; do
        for ((i=1; i<=req_detik; i++)); do
            hitungan=$((hitungan + 1))
            (
                start_time=$(date +%s%N)
                response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$target" 2>/dev/null)
                end_time_resp=$(date +%s%N)
                waktu=$((($end_time_resp - $start_time)/1000000))
                
                if [[ "$response" =~ ^(200|301|302|304)$ ]]; then
                    echo -e "${hijau}[✓] Req #$hitungan | HTTP $response | ${waktu}ms${nc}"
                elif [[ "$response" =~ ^(400|401|403|404|500|502|503)$ ]]; then
                    echo -e "${merah}[✗] Req #$hitungan | HTTP $response | ${waktu}ms${nc}"
                else
                    echo -e "${kuning}[?] Req #$hitungan | TIMEOUT | ${waktu}ms${nc}"
                fi
            ) &
        done
        wait
        echo -e "${cyan}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ [ $(date +%H:%M:%S) ] ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${nc}"
        sleep 1
    done
}

stress_test

echo ""
echo -e "${hijau}╔════════════════════════════════════════════════════════╗${nc}"
echo -e "${hijau}║  🎯  STRESS TEST COMPLETED!                            ║${nc}"
echo -e "${hijau}║  📊  Total Request : ${total_request}                                ║${nc}"
echo -e "${hijau}║  ⚠️   Untuk testing website sendiri / izin resmi saja   ║${nc}"
echo -e "${hijau}║  🛡️  Bertanggung jawab & Gunakan secara etis!          ║${nc}"
echo -e "${hijau}╚════════════════════════════════════════════════════════╝${nc}"
EOF

    chmod +x ~/stress_final.sh
    echo -e "${hijau}[✓] Script stress tester berhasil dibuat: ~/stress_final.sh${nc}"
    echo -e "${kuning}[!] Jalankan dengan: bash ~/stress_final.sh${nc}"
else
    echo -e "${hijau}[✓] ASCII art tersimpan di: ~/ascii_art/eagle_ascii.txt${nc}"
fi

echo ""
echo -e "${cyan}════════════════════════════════════════════════════════${nc}"
echo -e "${hijau}✨ Selesai! Logo kepala elang siap digunakan! ✨${nc}"
echo -e "${cyan}════════════════════════════════════════════════════════${nc}"
