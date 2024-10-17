from fastapi import HTTPException
from sqlalchemy.orm import Session
from scr.database.models import Post, Like
from scr.core_dir.schemas import PostBase


class CrudPost:
    @staticmethod
    def post_create_in_db(db: Session, data: PostBase):
        post = Post(title=data.title, content=data.content)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def post_put_db(id: int, data: PostBase, db: Session, ):
        post_query = db.query(Post).filter(Post.id == id).first()
        if post_query is None:
            raise HTTPException(status_code=404, detail="Post not found")
        post_query.title = data.title
        post_query.content = data.content
        db.commit()
        db.refresh(post_query)
        return post_query

    @staticmethod
    def post_delete_db(id: int, db: Session):
        post_query = db.query(Post).filter(Post.id == id).first()
        if post_query is None:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(post_query)
        db.commit()
        return {"detail": f"Post id {id} deleted successfully"}

    @staticmethod
    def post_get_db(id: int, db: Session):
        post_query = db.query(Post).filter(Post.id == id).first()
        if post_query is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return post_query

    @staticmethod
    def post_get_all_db(db: Session):
        posts = db.query(Post).all()
        if posts is None:
            raise HTTPException(status_code=404, detail="No posts found")
        return posts


class LikePostService:
    @staticmethod
    def like_post_db(id: int, db: Session):
        post = db.query(Post).filter(Post.id == id).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        like = Like(post_id=post.id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return like

    @staticmethod
    def delete_like_db(id: int, db: Session):
        like = db.query(Like).filter(Like.post_id == id).first()
        if like is None:
            raise HTTPException(status_code=404, detail="Post not found")
        db.delete(like)
        db.commit()
        return {"detail": f"Like in post {id} deleted successfully"}