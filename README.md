# Wypozyczalnia_ProjektPCz

## 1. Configuration instruction

1. Open project in PyCharm
2. Create virtual environment with python 3.12
3. Edit MONGO_URL variable in config.py file to contain valid connection string `(remember not to add this file with valid connection string to any future commits!)`
4. Install neccessary packages with 
```
pip install -r requirements.txt
```
5. Run project with
```
uvicorn main:app --reload
```