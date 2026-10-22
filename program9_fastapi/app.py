from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from html import escape

app = FastAPI(title="Personal Task Tracker")

app.add_middleware(
    SessionMiddleware,
    secret_key="change-this-to-a-long-random-secret"
)

# Database
engine = create_engine(
    "sqlite:///./tasks.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Task Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(300), default="")
    priority = Column(String(20), default="Medium")
    is_completed = Column(Boolean, default=False)
    created_by = Column(String(100), index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


Base.metadata.create_all(bind=engine)


# Login page
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("username"):
        return RedirectResponse("/", status_code=303)

    return """
    <html>
    <head><title>Login</title></head>
    <body style="font-family:Arial;max-width:400px;margin:60px auto">
        <h1>Personal Task Tracker</h1>
        <h3>Login</h3>
        <form action="/login" method="post">
            <input name="username" maxlength="100"
                   placeholder="Enter your name" required>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """


# Login
@app.post("/login")
def login(request: Request, username: str = Form(...)):
    username = username.strip()

    if not username or len(username) > 100:
        raise HTTPException(status_code=400, detail="Invalid username")

    request.session.clear()
    request.session["username"] = username

    return RedirectResponse("/", status_code=303)


# Home page
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    theme = request.cookies.get("theme", "light")
    if theme not in ("light", "dark"):
        theme = "light"

    db = SessionLocal()

    try:
        tasks = (
            db.query(Task)
            .filter(Task.created_by == username)
            .order_by(Task.created_at.desc())
            .all()
        )

        pending = [t for t in tasks if not t.is_completed]
        completed = [t for t in tasks if t.is_completed]

        def task_card(task):
            title = escape(task.title)
            description = escape(task.description or "")
            priority = escape(task.priority)

            return f"""
            <div class="task">
                <h3>{title}</h3>
                <p>{description}</p>
                <p>Priority: {priority}</p>
                <p>Created: {task.created_at.strftime('%d-%m-%Y %H:%M')}</p>
                <a href="/toggle/{task.id}">Toggle Status</a> |
                <a href="/edit/{task.id}">Edit</a>
                <form action="/delete/{task.id}" method="post"
                      style="display:inline"
                      onsubmit="return confirm('Delete this task?')">
                    <button class="delete" type="submit">Delete</button>
                </form>
            </div>
            """

        pending_html = "".join(task_card(t) for t in pending)
        completed_html = "".join(task_card(t) for t in completed)

        if not pending:
            pending_html = "<p>No pending tasks.</p>"

        if not completed:
            completed_html = "<p>No completed tasks.</p>"

        page = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Personal Task Tracker</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family:Arial,sans-serif;
                    max-width:850px;
                    margin:30px auto;
                    padding:15px;
                    background:THEME_BG;
                    color:THEME_TEXT;
                }
                .task, .form-box {
                    padding:18px;
                    margin:15px 0;
                    border-radius:10px;
                    background:THEME_CARD;
                    box-shadow:0 2px 7px #8883;
                }
                input, textarea, select {
                    width:100%;
                    padding:10px;
                    margin:7px 0;
                    box-sizing:border-box;
                }
                button, .btn {
                    padding:9px 12px;
                    background:#4f46e5;
                    color:white;
                    border:0;
                    border-radius:5px;
                    cursor:pointer;
                    text-decoration:none;
                }
                .delete { background:#dc2626; }
                a { color:#4f46e5; }
            </style>
        </head>
        <body>
            <h1>Personal Task Tracker</h1>
            <h3>Welcome, USERNAME</h3>

            <a class="btn" href="/set-theme/light">Light Theme</a>
            <a class="btn" href="/set-theme/dark">Dark Theme</a>
            <a class="btn" href="/logout">Logout</a>

            <div class="form-box">
                <h2>Add New Task</h2>
                <form action="/add" method="post">
                    <input name="title" maxlength="150"
                           placeholder="Task title" required>
                    <textarea name="description" maxlength="300"
                              placeholder="Description"></textarea>
                    <select name="priority">
                        <option>High</option>
                        <option selected>Medium</option>
                        <option>Low</option>
                    </select>
                    <button type="submit">Add Task</button>
                </form>
            </div>

            <h2>Pending Tasks (PENDING_COUNT)</h2>
            PENDING_TASKS

            <h2>Completed Tasks (COMPLETED_COUNT)</h2>
            COMPLETED_TASKS
        </body>
        </html>
        """

        bg = "#111827" if theme == "dark" else "#f1f5f9"
        fg = "#f9fafb" if theme == "dark" else "#0f172a"
        card = "#1f2937" if theme == "dark" else "#ffffff"

        page = (
            page.replace("THEME_BG", bg)
            .replace("THEME_TEXT", fg)
            .replace("THEME_CARD", card)
            .replace("USERNAME", escape(username))
            .replace("PENDING_COUNT", str(len(pending)))
            .replace("COMPLETED_COUNT", str(len(completed)))
            .replace("PENDING_TASKS", pending_html)
            .replace("COMPLETED_TASKS", completed_html)
        )

        return HTMLResponse(page)

    finally:
        db.close()


# Add task
@app.post("/add")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium")
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150 or len(description) > 300:
        raise HTTPException(status_code=400, detail="Invalid task details")

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(status_code=400, detail="Invalid priority")

    db = SessionLocal()
    try:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            is_completed=False,
            created_by=username,
            created_at=datetime.now()
        )
        db.add(task)
        db.commit()
    finally:
        db.close()

    return RedirectResponse("/", status_code=303)


# Toggle task status
@app.get("/toggle/{id}")
def toggle_task(id: int, request: Request):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    try:
        task = db.query(Task).filter(
            Task.id == id,
            Task.created_by == username
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.is_completed = not task.is_completed
        db.commit()
    finally:
        db.close()

    return RedirectResponse("/", status_code=303)


# Edit task page
@app.get("/edit/{id}", response_class=HTMLResponse)
def edit_task_page(id: int, request: Request):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    try:
        task = db.query(Task).filter(
            Task.id == id,
            Task.created_by == username
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        title = escape(task.title, quote=True)
        description = escape(task.description or "")
        priority = task.priority

        options = "".join(
            f'<option value="{p}" {"selected" if p == priority else ""}>{p}</option>'
            for p in ("High", "Medium", "Low")
        )

        return f"""
        <html>
        <head><title>Edit Task</title></head>
        <body style="font-family:Arial;max-width:500px;margin:40px auto">
            <h1>Edit Task</h1>
            <form action="/update/{task.id}" method="post">
                <label>Title</label>
                <input name="title" maxlength="150" value="{title}" required>
                <label>Description</label>
                <textarea name="description" maxlength="300">{description}</textarea>
                <label>Priority</label>
                <select name="priority">{options}</select>
                <button type="submit">Update Task</button>
            </form>
            <p><a href="/">Back to Home</a></p>
        </body>
        </html>
        """
    finally:
        db.close()


# Update task
@app.post("/update/{id}")
def update_task(
    id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("Medium")
):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    title = title.strip()
    description = description.strip()

    if not title or len(title) > 150 or len(description) > 300:
        raise HTTPException(status_code=400, detail="Invalid task details")

    if priority not in ("High", "Medium", "Low"):
        raise HTTPException(status_code=400, detail="Invalid priority")

    db = SessionLocal()
    try:
        task = db.query(Task).filter(
            Task.id == id,
            Task.created_by == username
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.title = title
        task.description = description
        task.priority = priority
        db.commit()
    finally:
        db.close()

    return RedirectResponse("/", status_code=303)


# Delete task
@app.post("/delete/{id}")
def delete_task(id: int, request: Request):
    username = request.session.get("username")

    if not username:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    try:
        task = db.query(Task).filter(
            Task.id == id,
            Task.created_by == username
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        db.delete(task)
        db.commit()
    finally:
        db.close()

    return RedirectResponse("/", status_code=303)


# Theme cookie
@app.get("/set-theme/{theme}")
def set_theme(theme: str, request: Request):
    if not request.session.get("username"):
        return RedirectResponse("/login", status_code=303)

    if theme not in ("light", "dark"):
        raise HTTPException(status_code=400, detail="Invalid theme")

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        key="theme",
        value=theme,
        max_age=30 * 24 * 60 * 60,
        httponly=True,
        samesite="lax"
    )
    return response


# Logout
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


# Run application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)