pip_install:
	pip install -U -r requirements/base.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn --default-timeout=100

assemble:
	pip install -U -r requirements/base.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn --default-timeout=100

start_simple_server:
	cd faker/servers && gunicorn  -w 2 -b 0.0.0.0:12345  simple_server:app --reload

test_simple_server:
	python tests/test_simple_server.py
