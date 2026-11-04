import asyncio, os, sys
from playwright.async_api import async_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1123, "height": 794})
        await pg.goto("file://" + os.path.join(HERE, "guide.html")); await pg.evaluate("document.fonts.ready"); await pg.wait_for_function("document.body.dataset.ready==='1'", timeout=10000); await pg.wait_for_timeout(400)
        os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
        n = await pg.evaluate("document.querySelectorAll('.pg').length")
        for i in range(n):
            el = (await pg.query_selector_all(".pg"))[i]
            await el.screenshot(path=os.path.join(HERE, "out", f"p{i+1:02d}.png"))
        if "--pdf" in sys.argv:
            await pg.emulate_media(media="print")
            await pg.pdf(path=sys.argv[sys.argv.index("--pdf")+1], width="297mm", height="210mm", print_background=True, margin={"top":"0","right":"0","bottom":"0","left":"0"})
        await b.close(); print("rendered", n)
asyncio.run(main())
