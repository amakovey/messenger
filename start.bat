@echo starting server
start python server.py
timeout 1
@echo starting clients 
start python client.py Andrey pass
start python client.py Misha pass
start python client.py Egor pass
start python client.py Sveta pass