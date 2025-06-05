import os
from PIL import Image

# アスキーアートに使用する文字セット（暗い -> 明るい）
ASCII_CHARS = "W#RE8xsi;,."

# 対応する画像ファイルの拡張子
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')


def generate_ascii_art(image_path, output_width, output_path):
    """`
    Args:
        image_path (str): 入力画像のファイルパス。
        output_width (int): 出力するアスキーアートの幅（文字数）。
        output_path (str): 出力するテキストファイルのパス。
    """
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"警告: ファイルが見つかりません: {image_path}")
        return
    except Exception as e:
        print(f"警告: ファイルを開けませんでした: {image_path} ({e})")
        return

    # 1. 画像のリサイズ
    original_width, original_height = img.size
    aspect_ratio_correction = 0.5
    new_height = int(original_height * (output_width /
                     original_width) * aspect_ratio_correction)
    if new_height <= 0:  # 高さが0以下になる場合はスキップ
        print(f"警告: 画像のサイズが小さすぎるためスキップします: {image_path}")
        return

    resized_img = img.resize((output_width, new_height))

    # 2. グレースケールに変換
    grayscale_img = resized_img.convert('L')

    # 3. アスキーアートに変換
    pixels = grayscale_img.getdata()
    ascii_str_list = []
    for pixel_value in pixels:
        index = int(pixel_value / 256 * len(ASCII_CHARS))
        if index == len(ASCII_CHARS):
            index = len(ASCII_CHARS) - 1
        ascii_str_list.append(ASCII_CHARS[index])

    # 画像の幅に合わせて改行を追加
    ascii_art = ""
    for i in range(0, len(ascii_str_list), output_width):
        ascii_art += "".join(ascii_str_list[i:i+output_width]) + "\n"

    # 4. テキストファイルとして保存
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(ascii_art)
    except IOError as e:
        print(f"エラー: ファイル書き込みに失敗しました: {output_path} ({e})")


def batch_convert_images(input_dir, output_width=400):
    """
    Args:
        input_dir (str): 画像が保存されているディレクトリのパス。
        output_width (int): 出力するアスキーアートの幅（文字数）。
    """
    # 1. 入力ディレクトリの存在確認
    if not os.path.isdir(input_dir):
        print(f"エラー: ディレクトリ '{input_dir}' が見つかりません。")
        return

    # 2. 出力ディレクトリを作成
    output_dir = f"{input_dir}_converted"
    os.makedirs(output_dir, exist_ok=True)
    print(f"出力先ディレクトリ: '{output_dir}'")

    # 3. ディレクトリ内のファイルを処理
    files = os.listdir(input_dir)
    image_files = [f for f in files if f.lower().endswith(
        SUPPORTED_EXTENSIONS)]

    if not image_files:
        print("ディレクトリ内に変換対象の画像ファイルが見つかりませんでした。")
        return

    print(f"{len(image_files)}個の画像ファイルを変換します...")

    for filename in image_files:
        input_path = os.path.join(input_dir, filename)

        # 出力ファイル名を生成
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_path = os.path.join(output_dir, output_filename)

        print(f"  変換中: {filename} -> {output_filename}")
        generate_ascii_art(input_path, output_width, output_path)

    print("\nすべての変換処理が完了しました。")


if __name__ == '__main__':
    INPUT_DIRECTORY = input("画像が保存されているフォルダのパスを入力してください: ")

    # アスキーアートの幅を指定
    ASCII_WIDTH = 200
    # --------------------------

    batch_convert_images(INPUT_DIRECTORY, ASCII_WIDTH)
