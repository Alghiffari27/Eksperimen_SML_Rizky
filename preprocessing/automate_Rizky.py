import pandas as pd
import numpy as np
import os
import argparse

def run_preprocessing(input_path, output_path):
    print("Mulai proses automasi preprocessing data stroke...")
    
    try:
        df = pd.read_csv(input_path)
        print(f"Berhasil memuat data dari: {input_path}")
    except Exception as e:
        print(f"Error memuat data: {e}")
        return

    if 'id' in df.columns:
        df = df.drop(columns=['id'])
        print("Kolom 'id' berhasil dihapus.")

    df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
    median_bmi = df['bmi'].median()
    df['bmi'] = df['bmi'].fillna(median_bmi)
    print("Missing values pada 'bmi' berhasil diimputasi dengan median.")

    df = df[df['gender'] != 'Other']
    
    df_encoded = pd.get_dummies(df, drop_first=True)
    print("Encoding variabel teks menjadi angka berhasil.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_encoded.to_csv(output_path, index=False)
    print(f"Data bersih berhasil disimpan ke: {output_path}\nSelesai!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Preprocessing Stroke Dataset")
    parser.add_argument('--input', type=str, default='../stroke_raw/healthcare-dataset-stroke-data.csv', help='Path ke data raw')
    parser.add_argument('--output', type=str, default='stroke_preprocessing/dataset_bersih.csv', help='Path ke output data bersih')
    
    args = parser.parse_args()
    run_preprocessing(args.input, args.output)