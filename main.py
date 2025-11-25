from flask import Flask, render_template, request
from playwright.async_api import async_playwright, ViewportSize
from playwright_stealth import Stealth
import asyncio
import uuid
import os
import json


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
_browser = None
_context = None
_page = None
_task_id = None

async def _init_browser():
    global _browser, _context, _page
    if _browser:
        return
    _playwright = await async_playwright().start()
    _browser = await _playwright.chromium.launch(headless=False)
    _context = await _browser.new_context()
    await Stealth().apply_stealth_async(_context)
    _page = await _context.new_page()
    await _page.set_viewport_size(ViewportSize({"width": 1024, "height": 1024}))


def create_app():
    app = Flask(__name__)
    loop.run_until_complete(_init_browser())

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.post("/load-and-start")
    def load_url():
        global _task_id
        url = request.form.get("url")
        task_prompt = request.form.get("task-prompt")
        _task_id = uuid.uuid4()

        task_dir = os.path.join(app.root_path, "static", str(_task_id))
        os.makedirs(task_dir, exist_ok=True)
        
        prompt_path = os.path.join(task_dir, "task_prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(task_prompt)
        
        image_path = os.path.join(task_dir, "start.png")
        loop.run_until_complete(screenshot(image_path, url))
        return render_template("partials/screenshot.html", task_id=str(_task_id), image_name="start")

    @app.post("/append-action")
    def append_action():
        global _task_id
        action_name = request.form.get("action-name")
        offset_x = request.form.get("offset-x", type=int)
        offset_y = request.form.get("offset-y", type=int)
        description = request.form.get("action-description")
        data = {
            "action_name": action_name,
            "offset_x": offset_x,
            "offset_y": offset_y,
            "description": description
        }

        action_id = uuid.uuid4()
        task_dir = os.path.join(app.root_path, "static", str(_task_id))

        loop.run_until_complete(apply_action(action_name, offset_x, offset_y))
        image_path = os.path.join(task_dir, f"{action_id}.png")
        loop.run_until_complete(screenshot(image_path))

        data["image_path"] = image_path
        action_path = os.path.join(task_dir, f"{action_id}.json")
        with open(action_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        return render_template("partials/screenshot.html", task_id=str(_task_id), image_name=action_id)
    
    @app.post("/accept-and-finish")
    def accept_and_finish():
        global _task_id
        final_answer = request.form.get("final-answer")

        task_dir = os.path.join(app.root_path, "static", str(_task_id))
        answer_path = os.path.join(task_dir, "final_answer.txt")
        with open(answer_path, "w", encoding="utf-8") as f:
            f.write(final_answer)

        return "<h1>Finished!</h1>"

    async def screenshot(path: str, url=None) -> str:
        await _page.evaluate("navigator.webdriver")
        if url:
            await _page.goto(url, wait_until="networkidle")
        await _page.screenshot(path=path)


    async def apply_action(action_name: str, offset_x: float, offset_y: float):
        if action_name == "click":
            await _page.mouse.click(offset_x, offset_y)
            await _page.wait_for_timeout(500)
            await _page.evaluate("navigator.webdriver")

        elif action_name == "scroll-down":
            await _page.mouse.wheel(0, 400)
            await _page.wait_for_timeout(500)
            await _page.evaluate("navigator.webdriver")

        elif action_name == "scroll-up":
            await _page.mouse.wheel(0, -400)
            await _page.wait_for_timeout(500)
            await _page.evaluate("navigator.webdriver")

    return app


app = create_app()
