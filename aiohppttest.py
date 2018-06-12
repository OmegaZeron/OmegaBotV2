import aiohttp

async def greet(name):
    return f"Howdy {name}!"

async def randomGreet(name):
    if len(name) > 4:
        message = await greet(name)
        print(message)

def run(coro):
    try:
        coro.send(None)
    except StopIteration as exc:
        print(exc.value)

run(randomGreet("PyCon"))
run(randomGreet("baz"))
