# coding:utf-8
import asyncio
import re
import os

import aiohttp
import aiofiles


class VolumeQueue(asyncio.Queue):
    def __init__(self, maxsize: int) -> None:
        super().__init__(maxsize=maxsize)
        self.volumeNotFound: bool = False

async def download_page_async(session: aiohttp.ClientSession, file_dir_url: str, page: int, imgs_path_prefix: str):
    img_path = f'{imgs_path_prefix}_{page}.jpg'
    if os.path.exists(img_path): # 已下载，跳过
        return
    url = f'{file_dir_url}/{page}.jpg'
    async with session.get(url=url) as resp:
        if resp.status == 200:
            img = await resp.read()
            async with aiofiles.open(img_path, mode='wb') as f:
                await f.write(img)
        else:
            raise NotImplementedError

async def download_volume_worker(session: aiohttp.ClientSession, base_url, book_id: int, volume_queue: VolumeQueue, imgs_dir: str):
    while True:
        volume_id = await volume_queue.get()
        volume_url = f'{base_url}/{book_id}/{book_id}{volume_id:03}'

        config_url = f'{volume_url}/mobile/javascript/config.js'
        async with session.get(url=config_url) as resp:
            if resp.status == 200:
                config = await resp.text()
                pages_num = int(re.search(r'bookConfig.totalPageCount=(\d+)', config).group(1))
                file_dir_url = f'{volume_url}/files/mobile'
                imgs_path_prefix = os.path.join(imgs_dir, f'{volume_id}')
                pages_coro = [download_page_async(session, file_dir_url, page, imgs_path_prefix) for page in range(1, pages_num + 1)]
                await asyncio.gather(*pages_coro)
                volume_queue.task_done()
            elif resp.status == 404:
                volume_queue.volumeNotFound = True
                volume_queue.task_done()
            else:
                raise NotImplementedError

async def download_book_async(base_url, book_id, imgs_dir):
    async with aiohttp.ClientSession() as session:
        volume_queue = VolumeQueue(maxsize=10)
        workers_num = 5
        # 创建并运行worker
        workers = [asyncio.create_task(download_volume_worker(session, base_url, book_id, volume_queue, imgs_dir)) for _ in range(workers_num)]

        # volume数量未知，不断加入workload保持队列满直到访问某个volume时404
        volume_id: int = 0
        while not volume_queue.volumeNotFound:
            await volume_queue.put(volume_id)
            volume_id += 1

        # 等待尚未完成的下载
        await volume_queue.join()

        # 销毁worker
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)

        

def download_book(book_category: int, book_id: str, download_dir):
    imgs_dir = os.path.join(download_dir, book_id)
    os.makedirs(imgs_dir, exist_ok=True)
    base_url = f'http://reserves.lib.tsinghua.edu.cn/book{book_category}'
    asyncio.run(download_book_async(base_url, book_id, imgs_dir))
    return imgs_dir