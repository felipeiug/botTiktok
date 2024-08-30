import pandas as pd
import os

input_dir = "F:/Downloads/cv-corpus-17.0-2024-03-15-pt/"
output_dir = 'tts/'

train_df = pd.read_csv(os.path.join(input_dir, 'train.tsv'), sep='\t')
val_df = pd.read_csv(os.path.join(input_dir, 'validated.tsv'), sep='\t')
test_df = pd.read_csv(os.path.join(input_dir, 'test.tsv'), sep='\t')

def prepare_data(df, split_name):
    with open(os.path.join(output_dir, f'{split_name}.csv'), mode='w+', encoding="UTF-8") as f:
        for _, row in df.iterrows():
            audio_path = os.path.join(input_dir, 'clips', row['path'])
            transcription = row['sentence']
            f.write(f"{audio_path}|{transcription}\n")

prepare_data(train_df, 'train')
prepare_data(val_df, 'validation')
prepare_data(val_df, 'test')
