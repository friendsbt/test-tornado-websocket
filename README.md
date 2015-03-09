`ws_client.py` 中 `p = pool.Pool(n)` 调整开启的websocket 数量

## 使用

开3个terminal/screen, 并保证mongo已经开启且监听默认端口

terminal 1: `$ python ws_server.py`  
terminal 2: `$ python ws_client.py`  
terminal 3: `$ ./boom_test.sh`