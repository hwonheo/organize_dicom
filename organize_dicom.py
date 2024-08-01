import os
import shutil
import pydicom
import re
import argparse

def sanitize_folder_name(name):
    sanitized_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name.replace(' ', '_'))
    return sanitized_name

def organize_dicom_by_series(input_folder):
    base_name = os.path.basename(os.path.normpath(input_folder))
    output_folder = os.path.join(input_folder, f"{base_name}_organized")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".dcm"):
                file_path = os.path.join(root, file)
                try:
                    ds = pydicom.dcmread(file_path)
                    series_name = ds.SeriesDescription if 'SeriesDescription' in ds else 'UnknownSeries'
                    protocol_name = ds.ProtocolName if 'ProtocolName' in ds else 'UnknownProtocol'
                    sanitized_series_name = sanitize_folder_name(series_name)
                    sanitized_protocol_name = sanitize_folder_name(protocol_name)
                    series_folder_name = f"{sanitized_series_name}_{sanitized_protocol_name}"
                    series_folder_path = os.path.join(output_folder, series_folder_name)
                    
                    if not os.path.exists(series_folder_path):
                        os.makedirs(series_folder_path)
                    
                    shutil.copy(file_path, os.path.join(series_folder_path, file))
                except Exception as e:
                    print(f"Failed to process file {file_path}: {e}")

def process_multiple_folders(base_input_folder):
    for folder_name in os.listdir(base_input_folder):
        folder_path = os.path.join(base_input_folder, folder_name)
        if os.path.isdir(folder_path):
            print(f"Processing folder: {folder_path}")
            organize_dicom_by_series(folder_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Organize DICOM files by series.')
    parser.add_argument('-b', '--base_input_folder', 
                        type=str, required=True, help='Path to the base input folder containing DICOM files.')
    args = parser.parse_args()
    process_multiple_folders(args.base_input_folder)
