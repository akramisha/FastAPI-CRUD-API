from fastapi import FastAPI, HTTPException, status
app = FastAPI() 

from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

# step 1
@app.get("/")  
def read_root():
    """Returns information about the Task API."""
    return{ "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] } 
    


@app.get("/health")  
def read_healthy():
    """Returns information about Health."""
    return{ "status": "ok" } 

# step 2

tasks = [
    {"id":1, "title":"Learn FastAPI", "done":True},
    {"id":2, "title":"Read Documentation", "done":False},
    {"id":3, "title":"Build CRUD API", "done":True},
]


@app.get("/tasks")
def read_tasks():
    """Returns information about the Task."""
    return tasks

@app.get("/tasks/{id}")
def read_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(
        status_code=404,
        detail=f"Task with id {id} not found"
    )

@app.get("/stats")
def status():
    done = 0
    total = len(tasks)
    for task in tasks:
        if task["done"]:
            done += 1
    open = total - done
    return {
                "total": total,
                 "done": done,
                 "open": open
            }
#-------------------------------------------------------------------------------------
# step 3
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    """Add information about the Task."""
    if not task.title or not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )
    new_task = {
        "id": tasks[-1]["id"] + 1,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task
    

# step 4
@app.put("/tasks/{id}")
def update_task(id: int, task: TaskUpdate):
    """Update information about the Task."""
    if not task.title or not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )
    for existing_task in tasks:
        if existing_task["id"] == id:
            existing_task["title"] = task.title
            existing_task["done"] = task.done
            return existing_task
    raise HTTPException(
        status_code=404,
        detail=f"Task with id {id} not found"
    )
    

@app.delete("/tasks/{id}", status_code=204)
def delete_task(id:int):
    """Delete information about the Task."""
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Task with id {id} not found"
    )


