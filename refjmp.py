import re
import fitz
import sys


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


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    add_links(input_file, output_file)

