from fastapi import FastAPI, Body, HTTPException, Depends
import uvicorn
from sqlalchemy.orm import Session
from scr.core_dir.schemas import PostBase, LikeBase, PostBaseWitID
from scr.core_dir.crud import CrudPost, LikePostService
from scr.database.db import Session_factory

app = FastAPI()


def get_db():
    db = Session_factory()
    try:
        yield db
    finally:
        db.close()


@app.post("/posts", response_model=PostBaseWitID, tags=["Добавление поста"])
def post_create_new(data: PostBase = Body(), db: Session = Depends(get_db)):
    """Создание нового поста"""
    try:
        post = CrudPost.post_create_in_db(db, data)
        return post
    except Exception as e:
        print(f"Ошибка при создании поста: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/posts/{id}", response_model=PostBaseWitID, tags=["Изменение поста"])
def post_update(id: int, data: PostBase = Body(), db: Session = Depends(get_db)):
    """Изменение поста"""
    try:
        put_post = CrudPost.post_put_db(id, data, db)
        return put_post
    except Exception as e:
        print(f"Ошибка при изменении поста: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/posts/{id}", tags=["Удаление поста"])
def post_delete(id: int, db: Session = Depends(get_db)):
    """Удаление поста"""
    try:
        delete_post = CrudPost.post_delete_db(id, db)
        return delete_post
    except Exception as e:
        print(f"Ошибка при удалении поста: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/posts/{id}", response_model=PostBase, tags=["Показать пост"])
def post_get(id: int, db: Session = Depends(get_db)):
    """Показать пост"""
    try:
        get_post = CrudPost.post_get_db(id, db)
        return get_post
    except Exception as e:
        print(f"Ошибка при получении поста: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/posts", response_model=list[PostBase], tags=["Показать все посты"])
def post_get_all(db: Session = Depends(get_db)):
    """Показать все посты"""
    try:
        get_posts_all = CrudPost.post_get_all_db(db)
        return get_posts_all
    except Exception as e:
        print(f"Ошибка при получении всех постов: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/posts/{id}/like", response_model=LikeBase, tags=["Поставить лайк на посту"])
def post_like(id: int, db: Session = Depends(get_db)):
    """Поставить лайк на пост"""
    try:
        like_post = LikePostService.like_post_db(id, db)
        return like_post
    except Exception as e:
        print(f"Ошибка при лайкинге поста: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.delete("/posts/{id}/like", tags=["Убрать лайк посту"])
def delete_post_like(id: int, db: Session = Depends(get_db)):
    """Убрать лайк посту"""
    try:
        delete_like_post = LikePostService.delete_like_db(id, db)
        return delete_like_post
    except Exception as e:
        print(f"Ошибка при удалении лайка поста: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
