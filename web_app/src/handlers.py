import pandas
import io
import pickle
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from sklearn.tree import DecisionTreeRegressor
from .database import get_db
from . import crud

router = APIRouter()


@router.get("/alive")
def get_alive():
    return


@router.post("/dataset")
def post_dataset(dataset: UploadFile, db: Session = Depends(get_db)):
    try:
        df = pandas.read_csv(dataset.file, sep=";")
    except pandas.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Input file is empty",
        )

    try:
        X = df.drop("y", axis=1)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="y is missing"
        )

    if X.empty:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="X is missing"
        )

    dataset.file.seek(0)
    data = dataset.file.read()
    db_dataset = crud.add_dataset(db, data)
    return {"id": db_dataset.id}


@router.post("/fit/{dataset_id}")
def post_fit(dataset_id: int, db: Session = Depends(get_db)):
    dataset = crud.get_dataset(db, dataset_id)
    if dataset is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found"
        )

    df = pandas.read_csv(io.BytesIO(dataset.data), sep=";")
    X = df.drop("y", axis=1)
    y = df["y"]
    model = DecisionTreeRegressor(max_depth=2)
    model.fit(X, y)
    serialized_model = pickle.dumps(model)
    db_model = crud.add_model(db, dataset, serialized_model)
    return {"id": db_model.id}


@router.get("/predict/{model_id}")
def get_predict(model_id: int, input_data: UploadFile, db: Session = Depends(get_db)):
    db_model = crud.get_model(db, model_id)
    if db_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Model not found"
        )

    try:
        X = pandas.read_csv(input_data.file, sep=";")
    except pandas.errors.EmptyDataError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Input file is empty",
        )

    model = pickle.loads(db_model.data)
    prediction = model.predict(X)
    return prediction.tolist()
