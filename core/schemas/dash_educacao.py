from pydantic import BaseModel



class DadosCsv(BaseModel):

    name : str
    csv_data : str

