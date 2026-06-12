from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,field_validator,computed_field
from typing import Annotated,Literal,Optional

class Client(BaseModel):
    id:Annotated[str,Field(...,description="Enter petiont id",examples=["P001"])]
    name:Annotated[str,Field(...,description="Enter petiont name",examples=['Luffy'])]
    city:Annotated[str,Field(...,description="Enter petiont city",examples=['wano'])]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Enter petiont age",examples=[19])]
    gender:Annotated[Literal["Male",'Female'],Field(...,description='Enter petiont gender',examples=['Male/female'])]
    height:Annotated[float,Field(...,description='Enter petiont height in mters',examples=[1.74])]
    weight:Annotated[float,Field(...,description='Enter petiont weight in kg',examples=[64])]

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, value):
        if isinstance(value, str):
            return value.capitalize()
        return value

    @computed_field
    @property
    def bmi(self) ->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <18:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'
class Client_update(BaseModel):
    name:Annotated[Optional [str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None)]
    gender:Annotated[Optional[Literal["Male",'Female']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None)]
    weight:Annotated[Optional[float],Field(default=None)]

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, value):
        if isinstance(value, str):
            return value.capitalize()
        return value

app=FastAPI()
@app.get("/")
def home():
    return {'message':'home page of functional api for clinic dataset'}
@app.get("/about")
def about():
    return {'message':'A fullyfunctional api for manage your petion record'}
def load_data():
    with open('data.json','r') as f:
        data=json.load(f)
    return data
def save(data):
    with open('data.json','w') as f:
        json.dump(data,f)
@app.get('/view')
def view():
    data=load_data()
    return data
@app.get('/patient/{patient_id}')
def id_data(patient_id:str = Path(...,description="Id of the patient in db",examples=["P001"])):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Db Not found")
@app.get('/sort')
def sort(sort_by:str=Query(...,description="sort on hight weight and bmp"),Order:str=Query('asc',description="ASC")):
    valid_field=['height','weight','bmi']
    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail="bad input by client")
    if Order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="bad input there not available asc and desc")
    data=load_data()
    sort_order=True if Order=="desc" else False
    sorted_data= sorted(data.values(), key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data
@app.post('/create')
def input(client:Client):
    data=load_data()
    if client.id in data:
        raise HTTPException(status_code=400)
    data[client.id]=client.model_dump(exclude={'id'})
    save(data)
    return JSONResponse(status_code=201,content={'message':'Your data are saved'})
@app.put('/update/{petiont_id}')
def update_value(pu:Client_update,petiont_id:str):
    data=load_data()
    if petiont_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    petiont_info=data[petiont_id]
    update_petiont_value=pu.model_dump(exclude_unset=True)
    for key,value in update_petiont_value.items():
        petiont_info[key]=value
    petiont_info["id"]=petiont_id
    petiont_obj=Client(**petiont_info)
    petiont_info=petiont_obj.model_dump(exclude={'id'})
    data[petiont_id]=petiont_info
    save(data)
    return JSONResponse(status_code=200,content={'message':'updated sucessfuly'})
@app.delete('/delete/{petiont_id}')
def delete_data(petiont_id:str):
    data=load_data()
    if petiont_id not in data:
        raise HTTPException(status_code=404,detail={'message':"Petiont not fount"})
    del data[petiont_id]
    save(data)
    return JSONResponse(status_code=200,content={'message':"Data deleted sucessfully"})
