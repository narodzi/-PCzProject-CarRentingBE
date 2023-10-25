# Wypozyczalnia_ProjektPCz

## 1. Configuration instruction

### Project without docker
1. Open project in PyCharm
2. Create virtual environment with python 3.11
3. Install neccessary packages with 
```
pip install -r requirements.txt
```
4. Set up MongoDB and Keycloak instances with docker
5. Run project with
```
uvicorn main:app --reload --host 0.0.0.0 --port 4300
```

### Keycloak
To create keycloak instance on docker run this command:
```
docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:22.0.4 start-dev
```

### MongoDB
To create MongoDB instance on docker run this command:
```
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

### Project on docker
To run this project with docker go to project path. Then use 
```
docker compose build
```
and next
```
docker compose up
```