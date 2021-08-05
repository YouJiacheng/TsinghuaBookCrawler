import os
import argparse
import time

from download_imgs import download_book
from save_pdf import save_pdf

def get_args():
    parser = argparse.ArgumentParser(description='Download e-book from http://reserves.lib.tsinghua.edu.cn. '
                                                 'By default, the temporary images will not be deleted ')

    parser.add_argument('book_category')
    parser.add_argument('book_id')
    parser.add_argument('--purge', help='Optional. Delete the temporary images.', action='store_true')

    args = parser.parse_args()
    book_category = args.book_category
    book_id = args.book_id
    purge = args.purge

    return book_category, book_id, purge


if __name__ == '__main__':
    book_category, book_id, purge = get_args()

    download_dir = 'download'

    started_at = time.monotonic()
    imgs_dir = download_book(book_category, book_id, download_dir)
    print(f'下载用时：{time.monotonic() - started_at:.2f} 秒')

    pdf_path = os.path.join(download_dir, f'{book_id}.pdf')

    started_at = time.monotonic()
    save_pdf(imgs_dir, pdf_path)
    print(f'保存用时：{time.monotonic() - started_at:.2f} 秒')



