import os

from fpdf import FPDF

def save_pdf(imgs_dir, pdf_path):
    pdf = FPDF()
    imgs_name_list = os.listdir(imgs_dir)
    imgs_name_list.sort()
    imgs_path_list = [os.path.join(imgs_dir, img_name) for img_name in imgs_name_list]
    for img_path in imgs_path_list[:20]:
        pdf.add_page()
        pdf.image(img_path, x=0, y=0, w=210, h=297)
    pdf.output(pdf_path)