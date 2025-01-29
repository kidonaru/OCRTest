import os
import argparse
from scripts.common_utils import load_image
from scripts.ocr_utils import ocr_image

def convert_to_tsv(ocr_result):
    # 行と列のグループ化のための閾値
    ROW_THRESHOLD = 10  # Y座標の差がこの値以内なら同じ行とみなす
    
    # まず、Y座標でグループ化
    y_groups = {}
    for line in ocr_result[0]:
        coords = line[0]
        text = line[1][0]
        y = coords[0][1]
        
        # 既存のグループに追加するか、新しいグループを作成
        grouped = False
        for base_y in y_groups.keys():
            if abs(y - base_y) <= ROW_THRESHOLD:
                y_groups[base_y].append((coords[0][0], text))
                grouped = True
                break
        if not grouped:
            y_groups[y] = [(coords[0][0], text)]
    
    # Y座標でソートしたグループを取得
    sorted_y = sorted(y_groups.keys())
    
    # 最初の行からX座標の基準位置を取得
    first_row = sorted(y_groups[sorted_y[0]], key=lambda x: x[0])
    column_x_positions = [item[0] for item in first_row]
    num_columns = len(column_x_positions)
    
    # 各行をX座標でソートして結果を作成
    rows = []
    for y in sorted_y:
        # 現在の行のアイテムをX座標でソート
        current_row_items = sorted(y_groups[y], key=lambda x: x[0])
        
        # 最も近い列位置にテキストを配置
        row = [''] * num_columns
        for x, text in current_row_items:
            # 最も近い列のインデックスを見つける
            closest_col = min(range(num_columns), 
                            key=lambda i: abs(x - column_x_positions[i]))
            if row[closest_col]:
                row[closest_col] += ' ' + text
            else:
                row[closest_col] = text
        
        rows.append(row)
    
    return '\n'.join(['\t'.join(row) for row in rows])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='画像からTSVファイルを生成します')
    parser.add_argument('input_path', help='入力画像のパス')
    parser.add_argument('--output', '-o', default='output.tsv',
                        help='出力TSVファイルのパス（デフォルト: output.tsv）')

    args = parser.parse_args()

    image = load_image(args.input_path)
    result = ocr_image(image, None, "japan")
    tsv_content = convert_to_tsv(result)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(tsv_content)

    print(f"TSVファイルを保存しました: {args.output}")
    print("内容:")
    print(tsv_content)
