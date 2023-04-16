import os
import re
import fitz
from flask import Flask, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import render_template

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制文件大小为16MB
CORS(app)

# 从上面的代码复制您的核心处理函数
def find_references(page_content):
    ref_regex = re.compile(r'\[\d+\]')
    return ref_regex.finditer(page_content)


def find_reference_location(doc, ref_num):
    ref_pattern = re.compile(rf'\[{ref_num}\]')
    matches = []
    for i in range(len(doc)):
        page = doc[i]
        content = page.get_text()
        ref_matches = ref_pattern.finditer(content)
        for match in ref_matches:
            areas = page.search_for(match.group())
            if areas:
                matches.append((i, areas[0]))

    if matches:
        return matches[-1]  # 返回最后一个匹配项作为参考文献位置
    else:
        return None, None


def add_links(input_file, output_file):
    # 读取PDF文件
    doc = fitz.open(input_file)

    # 遍历每一页
    for i in range(len(doc)):
        page = doc[i]
        content = page.get_text()
        ref_matches = find_references(content)

        # 处理每个匹配的引用编号
        for match in ref_matches:
            ref_num = int(match.group()[1:-1])
            areas = page.search_for(match.group())
            if areas:
                x0, y0, x1, y1 = areas[0]  # 使用匹配到的第一个坐标区域
                dest_page_num, dest_rect = find_reference_location(doc, ref_num)
                # print(dest_rect)
                if dest_page_num is not None and dest_rect is not None:
                    # 创建链接注释
                    link_annot = page.insert_link({
                        "kind": fitz.LINK_GOTO,
                        "from": fitz.Rect(x0, y0, x1, y1),
                        "to": fitz.Point(dest_rect[0], dest_rect[1]),
                        "page": dest_page_num,
                    })

    # 保存新的PDF文件
    doc.save(output_file)
    doc.close()


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_file_path)
            output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f'output_{filename}')
            add_links(input_file_path, output_file_path)
            return redirect(url_for('download_file', filename=f'output_{filename}'))


@app.route('/download/<filename>')
def download_file(filename):
    response = send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)
    response.headers['Location'] = f"/download/{filename}"
    return response


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    app.run(debug=True)
