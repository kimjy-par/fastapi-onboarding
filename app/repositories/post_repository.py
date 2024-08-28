from contextlib import AbstractContextManager, AbstractAsyncContextManager
from typing import Callable, List
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException

from app.models.post import Post
from app.models.user import User
from app.schemas.post_schema import UpdatePostSchema


class PostRepository():
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory

    def get_by_id(self, id: int) -> Post:
        with self.session_factory() as session:
            query = session.query(Post).filter(Post.id == id).first()
            if not query:
                raise
            
            return query
        
    def get_all_by_user_id(self, user_id) -> List[Post]:
        with self.session_factory() as session:
            query = session.query(Post).filter(Post.user_id==user_id)

            return {'results': query}
        
    def create_post_with_user(self, post: Post) -> Post:
        with self.session_factory() as session:
            session.add(post)
            session.commit()
            session.refresh(post)

            return post
        
    def update_post(self, id, schema: UpdatePostSchema) -> Post:
        with self.session_factory() as session:
            session.query(Post).filter(Post.id == id).update(schema.model_dump(exclude_none=True))
            session.commit()
            return self.get_by_id(id)

    def delete_post(self, id) -> None:
        with self.session_factory() as session:
            query = session.query(Post).filter(Post.id == id).first()
            if not query:
                raise

            session.delete(query)
            session.commit()


class AsyncPostRepository():
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def get_by_id(self, id: int) -> Post:
        async with self.session_factory() as session:
            results = await session.execute(select(Post).filter(Post.id == id).limit(1))
            post = results.scalars().first()
            
            return post
        

    async def create_post_with_user(self, post: Post) -> Post:
        async with self.session_factory() as session:
            session.add(post)
            raise HTTPException(status_code=400, detail="Forced exception")
            await session.commit()
            return await session.refresh(post)