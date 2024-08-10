"""
将docx格式的文档转换成md格式的文档
"""
import os
import re

import docx
from docx import Document
import json
from loguru import logger
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.text.paragraph import Paragraph
from docx.parts.image import ImagePart
import xml.etree.ElementTree as ET
from PIL import Image


def handle_picture(part):
    '''
    处理保存的图片转化成md可显示的png图片
    :param part:
    :return:
    '''
    try:
        os.makedirs("../../utils/img_ori", exist_ok=True)
        print(f"文件夹 img_ori 已存在或已创建")
    except OSError as e:
        print(f"创建文件夹时出错: {e.strerror}")
    try:
        os.makedirs("../../utils/img_jpeg", exist_ok=True)
        print(f"文件夹 img_ori 已存在或已创建")
    except OSError as e:
        print(f"创建文件夹时出错: {e.strerror}")
    img_name = part.partname.split('/')[-1]
    logger.info(img_name)
    # 将原始图片保存起来
    with open(f'img_ori/{img_name}', "wb") as f:
        f.write(part.blob)
    ext = img_name.split('.')[-1]
    vector_exts = ['emf', 'wmf', 'svg', 'eps', 'ai']  # 矢量图
    if ext in vector_exts:
        # 如果是矢量图则转成jpeg在md显示
        img = Image.open(f'img_ori/{img_name}')
        img.save(f"img_jpeg/{img_name.split('.')[0]}.png", "JPEG")
        img_name = f"{img_name.split('.')[0]}.png"
    else:
        with open(f'img_jpeg/{img_name}', "wb") as f:
            f.write(part.blob)
    return f"![图片](img_jpeg/{img_name})"

def is_embed(para: Paragraph, doc: Document):
    root = ET.fromstring(para._element.xml)
    for elem in root.iter():
        if elem.tag.endswith("OLEObject"):
            embed_id = elem.attrib.get("Type")
            rid = None
            for imagedata_elem in root.findall(".//{urn:schemas-microsoft-com:vml}imagedata"):
                rid = imagedata_elem.attrib.get(
                    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            if rid and embed_id == "Embed":
                part = doc.part.related_parts[rid]
                logger.info(part)
                return part
    return None


def is_image(para: Paragraph, doc: Document):
    images = para._element.xpath('.//pic:pic')  # 获取所有图片
    for image in images:
        for img_id in image.xpath('.//a:blip/@r:embed'):  # 获取图片id
            part = doc.part.related_parts[img_id]  # 根据图片id获取对应的图片
            logger.info(part)
            if isinstance(part, ImagePart):
                return part
    return None


def table_to_markdown(serial_num, document):
    markdown_rows = []
    for row in document.tables[serial_num - 1].rows:
        cells = [cell.text for cell in row.cells]
        new_cells = [cells_word.replace('\n', '<br>') for cells_word in cells]
        markdown_row = '| ' + ' | '.join(new_cells) + ' |\n'
        # 添加 Markdown 样式的行分隔符
        if len(markdown_rows) == 1:
            markdown_rows.append('|' + ' --- |' * len(cells) + '\n')
        markdown_rows.append(markdown_row)
    return ''.join(markdown_rows)


def docx_to_markdown(docx_name, markdown_name):
    doc = Document(docx_name)
    logger.info(f"文档打开完成{doc}")

    with open(markdown_name, 'w', encoding='utf-8') as md_file:
        last_paragraph_was_table = False
        table_serial_number = 0
        for element in doc.element.body.iterchildren():
            logger.debug(element)
            last_paragraph_was_table = False
            if isinstance(element, CT_Tbl):
                table_serial_number += 1
                table = table_to_markdown(table_serial_number, doc)
                md_file.write(table + '\n\n')
                last_paragraph_was_table = True
                logger.debug(f"Table: Converted.")
            elif isinstance(element, CT_P):
                paragraph = Paragraph(element, doc)
                # 图像判断
                img_TF = is_image(paragraph, doc)
                if img_TF:
                    md_file.write(
                        "[链接](img_ori" + img_TF.partname.split('/')[-1] + ')\n\n图像占位符：balabala\n\n' + handle_picture(img_TF))
                # 嵌入体判断
                embed = is_embed(paragraph, doc)
                if embed:
                    md_file.write(
                        "[链接](img_ori" + embed.partname.split('/')[-1] + ')\n\n图像占位符：balabala\n\n' + handle_picture(embed))

                # 文本操作
                if last_paragraph_was_table:
                    md_file.write('\n')  # 在表格后加一行空行以模仿原始文档中的空白
                if paragraph.style.name.startswith('Heading'):
                    # 根据样式名判断标题级别并转换为Markdown标题
                    level = int(paragraph.style.name[-1])
                    md_file.write(f"{'#' * level} {paragraph.text}\n\n")
                    logger.debug(f"Heading {level}: {paragraph.text}")
                elif paragraph.style.name == 'List Bullet':
                    md_file.write(f"* {paragraph.text}\n")
                    logger.debug(f"List Bullet: {paragraph.text}")
                elif paragraph.style.name == 'List Number':
                    md_file.write(f"1. {paragraph.text}\n")
                    logger.debug(f"List Number: {paragraph.text}")
                else:
                    md_file.write(paragraph.text.replace('\n', ' ') + '\n\n')
                last_paragraph_was_table = False



if __name__ == '__main__':
    # docx_name = r"D:\project\cosmetic-langchain-llm\unstructured_data\29531-i10.docx"
    docx_path = r"C:\Users\林新锋\Desktop\EMBED VisioViewer.docx"
    markdown_path = r'md'
    docx_to_markdown(docx_path, markdown_path)
