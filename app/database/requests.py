from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete, desc
from decimal import Decimal


async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id, tokens_for_NoD='0', tokens_for_NoPY='0', username=username))
            await session.commit()
            return False
        return True if user.name else False
    
async def is_user(username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))
        
        if not user:
            return False
        return True

async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
    
async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))
    
async def get_user_by_username(username):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.username == username))

async def update_user(tg_id, name):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(name=name))
        await session.commit()


async def add_tokens_NoD(username, tokens_count):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))
        new_tokens_count = Decimal(Decimal(user.tokens_for_NoD) + Decimal(tokens_count))
        
        await session.execute(update(User).where(User.id == user.id).values(tokens_for_NoD=str(new_tokens_count)))
        await session.commit()
        
async def add_tokens_NoPY(username, tokens_count):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))
        new_tokens_count = Decimal(Decimal(user.tokens_for_NoPY) + Decimal(tokens_count))
        
        await session.execute(update(User).where(User.id == user.id).values(tokens_for_NoPY=str(new_tokens_count)))
        await session.commit()


async def calculate_NoD(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        new_tokens_balance = Decimal(Decimal(user.tokens_for_NoD) - 1)
        
        await session.execute(update(User).where(User.id == user.id).values(tokens_for_NoD=str(new_tokens_balance)))
        await session.commit()
        
async def calculate_NoPY(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        new_tokens_balance = Decimal(Decimal(user.tokens_for_NoPY) - 1)
        
        await session.execute(update(User).where(User.id == user.id).values(tokens_for_NoPY=str(new_tokens_balance)))
        await session.commit()