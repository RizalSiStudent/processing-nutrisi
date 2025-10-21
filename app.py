import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from flask import Flask, render_template

# ===============================================
# 1. FUNGSIONALITAS ANALISIS & PLOTTING
# ===============================================

def generate_plots(df):
    """Menghasilkan semua visualisasi dan menyimpannya sebagai file gambar."""
    
    # Pastikan folder static ada
    import os
    if not os.path.exists('static'):
        os.makedirs('static')

    # --- Grafik 1: Perbandingan Abon vs Ayam (Bar Plot) ---
    abon_df = df[df['name'].str.contains('Abon', case=False, na=False)]
    ayam_df = df[df['name'].str.contains('Ayam', case=False, na=False)]
    
    abon_mean = abon_df[['calories', 'fat', 'carbohydrate', 'proteins']].mean()
    ayam_mean = ayam_df[['calories', 'fat', 'carbohydrate', 'proteins']].mean()
    
    compare_df = pd.DataFrame({'Abon': abon_mean, 'Ayam': ayam_mean})

    plt.figure(figsize=(8,5))
    compare_df.plot(kind='bar')
    plt.title('Perbandingan Kandungan Gizi: Abon vs Ayam')
    plt.ylabel('Jumlah (gram atau kkal)')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Makanan')
    plt.tight_layout()
    plt.savefig('static/perbandingan_abon_ayam.png')
    plt.close()

    # --- Grafik 2: Top 5 Kalori (Bar Plot) ---
    top5_calories = df.nlargest(5, 'calories')[['name', 'calories', 'fat', 'carbohydrate', 'proteins']]

    plt.figure(figsize=(10,6))
    top5_calories.set_index('name')[['calories', 'fat', 'carbohydrate', 'proteins']].plot(kind='bar')
    plt.title('Top 5 Makanan dengan Kalori Tertinggi dan Kandungan Gizinya')
    plt.ylabel('Jumlah (gram atau kkal)')
    plt.xticks(rotation=30, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Kandungan Gizi')
    plt.tight_layout()
    plt.savefig('static/top5_kalori.png')
    plt.close()
    
    # --- Grafik 3: Perbandingan Kalori 5 Makanan Populer (Pie/Donut Chart) ---
    foods = ['Abon','Ayam','Telur','Ikan','Tahu']
    # Catatan: Karena Anda menggunakan .sum() di notebook, saya pertahankan.
    gizi = df[df['name'].isin(foods)].groupby('name')[['calories','fat','carbohydrate','proteins']].sum()

    plt.figure(figsize=(6,6))
    plt.pie(gizi['calories'], labels=gizi.index, autopct='%1.1f%%',
            startangle=140, wedgeprops={'width':0.4})
    plt.title('Perbandingan Kalori 5 Makanan Populer')
    plt.tight_layout()
    plt.savefig('static/perbandingan_5_makanan_pie.png')
    plt.close()

    # --- Grafik 4: Top 5 Lemak (Scatter Plot) ---
    top5_fat = df.nlargest(5, 'fat')

    plt.figure(figsize=(8,6))
    plt.scatter(top5_fat['name'], top5_fat['fat'], color='orange', s=150, edgecolors='black')

    plt.title('5 Makanan dengan Lemak Tertinggi', fontsize=14, weight='bold')
    plt.xlabel('Nama Makanan', fontsize=12)
    plt.ylabel('Lemak (gram)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('static/top5_lemak.png')
    plt.close()


# ===============================================
# 2. FLASK WEB APP
# ===============================================

app = Flask(__name__)

# --- Load Data dan Generate Plot di Awal ---
try:
    data_df = pd.read_csv("nutrition.csv")
    # Panggil fungsi untuk membuat semua file gambar
    generate_plots(data_df)
    print("Semua grafik berhasil dibuat dan disimpan di folder static.")
except FileNotFoundError:
    print("ERROR: File nutrition.csv tidak ditemukan!")
    data_df = None
except Exception as e:
    print(f"ERROR saat memproses data/membuat grafik: {e}")
    data_df = None


@app.route('/')
def home():
    # List nama file gambar yang sudah kita simpan di folder static
    plot_files = {
        'abon_ayam': 'perbandingan_abon_ayam.png',
        'top5_kalori': 'top5_kalori.png',
        'pie_kalori': 'perbandingan_5_makanan_pie.png',
        'top5_lemak': 'top5_lemak.png',
    }
    
    # Anda juga bisa mengambil data tabel hasil processing (seperti compare_df)
    # untuk ditampilkan dalam format HTML
    
    return render_template('dashboard.html', plots=plot_files)

# --- Ini hanya untuk dijalankan di lingkungan lokal VS Code/Komputer ---
# if __name__ == '__main__':
#     # Pastikan Anda menginstal Flask: pip install Flask
#     app.run(debug=True)