import csv
import os
from datetime import datetime

FILE_BUAH = 'buah.csv'
FILE_TRANSAKSI = 'transaksi.csv'

def init_file():
    if not os.path.exists(FILE_BUAH):
        with open(FILE_BUAH, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['nama', 'harga', 'jumlah'])

    if not os.path.exists(FILE_TRANSAKSI):
        with open(FILE_TRANSAKSI, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['tanggal', 'jenis', 'nama', 'jumlah', 'total'])

def tambah_buah():
    nama = input("Nama buah: ")
    harga = int(input("Harga: "))
    jumlah = int(input("Jumlah: "))

    with open(FILE_BUAH, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([nama, harga, jumlah])
    print("✅ Buah berhasil ditambahkan.")

def tampilkan_buah():
    print("\n📦 Daftar Buah:")
    with open(FILE_BUAH, mode='r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
        if not data:
            print("Belum ada buah yang terdaftar.")
        for row in data:
            print(f"{row['nama']} - Harga: Rp{row['harga']} - Stok: {row['jumlah']}")

def jual_buah():
    nama = input("Nama buah yang dijual: ")
    jumlah_jual = int(input("Jumlah: "))
    baris = []
    found = False

    with open(FILE_BUAH, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['nama'].lower() == nama.lower():
                found = True
                if int(row['jumlah']) < jumlah_jual:
                    print("❌ Stok tidak mencukupi!")
                    return
                row['jumlah'] = str(int(row['jumlah']) - jumlah_jual)
                total = int(row['harga']) * jumlah_jual
                simpan_transaksi("jual", nama, jumlah_jual, total)
            baris.append(row)

    if not found:
        print("❌ Buah tidak ditemukan.")
        return

    with open(FILE_BUAH, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['nama', 'harga', 'jumlah'])
        writer.writeheader()
        writer.writerows(baris)

    print("✅ Penjualan berhasil dicatat.")

def beli_buah():
    nama = input("Nama buah yang dibeli: ")
    jumlah_beli = int(input("Jumlah: "))
    harga_baru = int(input("Harga beli per buah: "))
    baris = []
    found = False

    with open(FILE_BUAH, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['nama'].lower() == nama.lower():
                found = True
                row['jumlah'] = str(int(row['jumlah']) + jumlah_beli)
                row['harga'] = str(harga_baru)
                total = harga_baru * jumlah_beli
                simpan_transaksi("beli", nama, jumlah_beli, total)
            baris.append(row)

    if not found:
        with open(FILE_BUAH, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([nama, harga_baru, jumlah_beli])
        simpan_transaksi("beli", nama, jumlah_beli, harga_baru * jumlah_beli)
        print("✅ Buah baru ditambahkan dan dicatat sebagai pembelian.")
        return

    with open(FILE_BUAH, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['nama', 'harga', 'jumlah'])
        writer.writeheader()
        writer.writerows(baris)

    print("✅ Pembelian berhasil dicatat.")

def simpan_transaksi(jenis, nama, jumlah, total):
    with open(FILE_TRANSAKSI, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), jenis, nama, jumlah, total])

def tampilkan_transaksi():
    print("\n📒 Daftar Transaksi:")
    if not os.path.exists(FILE_TRANSAKSI):
        print("Belum ada transaksi.")
        return

    with open(FILE_TRANSAKSI, mode='r') as f:
        reader = csv.DictReader(f)
        transaksi_ditemukan = False
        for row in reader:
            if row and all(row.values()):  # Cegah error dari baris kosong
                transaksi_ditemukan = True
                print(f"{row['tanggal']} - {row['jenis']} - {row['nama']} - {row['jumlah']} buah - Rp{row['total']}")

        if not transaksi_ditemukan:
            print("Belum ada transaksi yang dicatat.")

def menu():
    while True:
        print("\n=== Menu Toko Buah ===")
        print("1. Tambah Buah")
        print("2. Tampilkan Buah")
        print("3. Jual Buah")
        print("4. Beli Buah")
        print("5. Lihat Transaksi")
        print("6. Keluar")
        pilihan = input("Pilih: ")

        if pilihan == '1':
            tambah_buah()
        elif pilihan == '2':
            tampilkan_buah()
        elif pilihan == '3':
            jual_buah()
        elif pilihan == '4':
            beli_buah()
        elif pilihan == '5':
            tampilkan_transaksi()
        elif pilihan == '6':
            print("Terima kasih! Program selesai.")
            break
        else:
            print("❗ Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    init_file()
    menu()
