import os
import random
import shutil
import string
from PIL import Image
import pandas as pd
import cv2

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def randomname(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def get_tmp_dir():
    tmp_dir = os.path.join(".", "tmp")
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    return tmp_dir

def get_tmp_file_name(ext):
    if ext[0] != ".":
        ext = "." + ext
    return randomname(10) + ext

def get_tmp_file_path(ext):
    tmp_dir = get_tmp_dir()
    tmp_file_name = get_tmp_file_name(ext)
    tmp_file_path = os.path.join(tmp_dir, tmp_file_name)
    return tmp_file_path

def create_new_tmp_dir():
    tmp_dir = get_tmp_dir()
    tmp_dir_name = randomname(10)
    tmp_dir_path = os.path.join(tmp_dir, tmp_dir_name)
    os.mkdir(tmp_dir_path)
    return tmp_dir_path

def load_image(image_path, safety=False):
    image = None

    if safety:
        tmp_image_path = get_tmp_file_path(".png")
        shutil.copy(image_path, tmp_image_path)
        image = cv2.imread(tmp_image_path)
        os.remove(tmp_image_path)
    else:
        image = cv2.imread(image_path)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def save_image(image, image_path):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(image_path, image)

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    aspect_ratio = width / height
    
    # ターゲットのサイズとアスペクト比を設定
    target_width = int(size[0])
    target_height = int(size[1])
    target_ratio = target_width / target_height

    if aspect_ratio > target_ratio:
        # 元の画像の方が横長
        new_width = target_width
        new_height = round(target_width / aspect_ratio)
    else:
        # 元の画像の方が縦長またはアスペクト比が等しい
        new_height = target_height
        new_width = round(target_height * aspect_ratio)
    
    resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # 新しい画像を作成して黒で塗りつぶす
    new_image = Image.new("RGB", (target_width, target_height), "black")
    # リサイズした画像を新しい画像の中央に配置
    new_image.paste(resized_image, ((target_width - new_width) // 2, (target_height - new_height) // 2))

    # 画像を保存
    new_image.save(output_image_path, quality = 85)

def format_short_chara_name(chara_name: str):
    if '（' in chara_name and '）' in chara_name:
        return chara_name.split('（')[0] + chara_name.split('）')[1]
    return chara_name

def save_timeline(project_path: str, dataframe: pd.DataFrame):
    tsv_path = os.path.join(project_path, "timeline.tsv")
    dataframe.to_csv(tsv_path, sep='\t', index=False)

    return tsv_path

def load_timeline(project_path: str):
    tsv_path = os.path.join(project_path, "timeline.tsv")
    if not os.path.exists(tsv_path):
        return None

    return pd.read_csv(tsv_path, sep='\t', dtype=str)

def save_memo(project_path: str, memo: str):
    memo_path = os.path.join(project_path, "memo.txt")
    with open(memo_path, "w", encoding="utf-8") as f:
        f.write(memo)

    return memo_path

def load_memo(project_path: str):
    memo_path = os.path.join(project_path, "memo.txt")
    if not os.path.exists(memo_path):
        return ""

    with open(memo_path, "r", encoding="utf-8") as f:
        memo = f.read()

    return memo

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def calculate_similarity(s1, s2):
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    similarity = (max_len - distance) / max_len
    return similarity * 100

def str_to_time(time_text: str):
    if time_text == "":
        return 0
    time = int(time_text.split(":")[0]) * 60 + float(time_text.split(":")[1])
    return time

def time_to_str(time: float):
    milliseconds = int(round(time * 1000))
    minutes = milliseconds // (1000 * 60)
    seconds = (milliseconds // 1000) % 60
    return f"{minutes:02}:{seconds:02}.{milliseconds % 1000:03}"

# 誤認しやすい文字の変換テーブル
ocr_conversion = str.maketrans(
    "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
    "ガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポ"
    "シソぁぃぅぇぉゎっゃゅょァィゥェォヮッャュョ"
    "三一－-",
    "かきくけこさしすせそたちつてとはひふへほはひふへほ"
    "カキクケコサツスセソタチツテトハヒフヘホハヒフヘホ"
    "ツンあいうえおわつやゆよアイウエオワツヤユヨ"
    "二ーーー",
    "゛゜！!？?～~、。.　 ♡："
)

def convert_ocr_string(text):
    text = text.translate(ocr_conversion)
    return text

safe_filename_conversion = str.maketrans(
    "\\/:*?\"<>|", "￥／：＊？”＜＞｜"
)

def convert_safe_filename(text):
    text = text.translate(safe_filename_conversion)
    return text
