export ENV=prod
# export ENV=dev
export RECEIVERS='139959086@qq.com'
nohup python3 main.py > run.log 2>&1 &