import hashlib
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from .database import Dataset, Model


def get_dataset(db: Session, dataset_id: int):
    try:
        return db.query(Dataset).filter(Dataset.id == dataset_id).one()
    except NoResultFound:
        return


def get_dataset_by_hash(db: Session, md5_hash: str):
    try:
        return db.query(Dataset).filter(Dataset.md5_hash == md5_hash).one()
    except NoResultFound:
        return


def add_dataset(db: Session, dataset: bytes):
    md5_hash = hashlib.md5(dataset).hexdigest()
    db_dataset = get_dataset_by_hash(db, md5_hash)
    if db_dataset is not None:
        return db_dataset

    try:
        db_dataset = Dataset(data=dataset, md5_hash=md5_hash)
        db.add(db_dataset)
        db.commit()
        return db_dataset
    except SQLAlchemyError:
        db.rollback()
        raise


def get_model(db: Session, model_id: int):
    try:
        return db.query(Model).filter(Model.id == model_id).one()
    except NoResultFound:
        return


def get_model_by_hash(db: Session, md5_hash: str):
    try:
        return db.query(Model).filter(Model.md5_hash == md5_hash).one()
    except NoResultFound:
        return


def add_model(db: Session, dataset: Dataset, model: bytes):
    md5_hash = hashlib.md5(model).hexdigest()
    db_model = get_model_by_hash(db, md5_hash)
    if db_model is not None:
        return db_model

    try:
        db_model = Model(dataset=dataset, data=model, md5_hash=md5_hash)
        db.add(db_model)
        db.commit()
        return db_model
    except SQLAlchemyError:
        db.rollback()
        raise
