import pandas as pd
from pathlib import Path

SRC = Path("excel/wedago_kuliner_master_final.xlsx")
OUT = Path("csv"); OUT.mkdir(parents=True, exist_ok=True)

# Hanya 3 sheet ini yang dipublish
SHEETS = {
    "Promo": "promo.csv",
    "Kategori": "kategori.csv",
    "Data": "data.csv",
}

# Validasi minimal biar admin gak salah sheet/kolom
REQUIRED_DATA_COLS = [
    "Nama","Deskripsi","Harga","Stok","image_url",
    "action_url","web_url","Toko","Mitra",
    "Nama Menu","Menu","kategori_pilihan",
    "subcat_primary"  # admin boleh ubah manual
]

xl = pd.ExcelFile(SRC)
for sheet, fname in SHEETS.items():
    if sheet not in xl.sheet_names:
        raise SystemExit(f"Sheet '{sheet}' tidak ada di {SRC.name}")

    df = pd.read_excel(SRC, sheet_name=sheet)

    if sheet == "Data":
        # Pastikan kolom kunci ada
        missing = [c for c in REQUIRED_DATA_COLS if c not in df.columns]
        if missing:
            raise SystemExit(f"Sheet Data kurang kolom: {missing}")
        # Bersihkan NaN jadi string kosong untuk teks
        text_cols = [c for c in df.columns if df[c].dtype == 'object']
        for c in text_cols: df[c] = df[c].fillna("")
        # Pastikan angka tidak 'NaN' di CSV
        num_cols = ["Harga","Stok"]
        for c in num_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")

    df.to_csv(OUT / fname, index=False, encoding="utf-8")

print("✅ CSV generated di folder /csv")
