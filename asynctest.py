import asyncio

async def findDivisibles(inRange, divBy):
    print("Findinf nums in range {} divisible by {}".format(inRange, divBy))
    located = []
    for i in range(inRange):
        if i % divBy == 0:
            located.append(i)
        if i % 50000 == 0:
            await asyncio.sleep(.000001)
    print("Done with nums in range {} divisible by {}".format(inRange, divBy))
    return located

async def main():
    divs1 = loop.create_task(findDivisibles(508000, 34113))
    divs2 = loop.create_task(findDivisibles(100052, 3210))
    divs3 = loop.create_task(findDivisibles(500, 3))
    await asyncio.wait([divs1, divs2, divs3])
    return divs1, divs2, divs3

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        d1, d2, d3 = loop.run_until_complete(main()) #run_forever for my bot?
        print(d1.result())
    except Exception as e:
        print(str(e))
    finally:
        loop.close()