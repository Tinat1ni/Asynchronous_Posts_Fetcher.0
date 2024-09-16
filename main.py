import asyncio
import aiohttp
import json

lock = asyncio.Lock()

async def get_post(post_id, file):
     url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
     async with aiohttp.ClientSession() as session:
          async with session.get(url, ssl = False) as response:
               data = await response.json()
               async with lock:
                    with open(file, 'a') as f:
                         if f.tell() == 0:
                              f.write('[')
                         else:
                              f.write(', ')
                         json.dump(data, f, indent = 4)


async def main():
     file = 'data.json'
     tasks = []
     post_ids = range(1,78)

     with open(file, 'w') as f:
          f.write('')

     for post_id in post_ids:
          tasks.append(asyncio.create_task(get_post(post_id, file)))
     await asyncio.gather(*tasks)

     with open(file, 'a') as f:
          f.write(']')


if __name__ == '__main__':
     asyncio.run(main())