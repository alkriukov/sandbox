import asyncio

async def reach(name):
    print('Start reaching', name)
    await asyncio.sleep(len(name))
    print('Reached', name)

async def main():
    my_family = ['Nika', 'Maxim', 'Vladislav', 'Olga', 'Alexey']
    hello_tasks = []
    for name in my_family:
        task = asyncio.create_task(reach(name))
        print(type(task))
        hello_tasks.append(task)
    for hello in hello_tasks:
        await hello        

asyncio.run(main())
