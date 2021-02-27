import sys
import os


sys.stdout = sys.stderr
bind  = "0.0.0.0:"+str(os.environ.get("PORT", "5000"))
print (bind)
workers =int(os.environ.get('WORKER_COUNT',1))
print ('No of workers ' , workers)
timeout = 600

running_mode = os.environ.get('USE_SAGEMAKER', 0)

if running_mode == 1:
    print("running_mode : SageMaker")
else:
    print("running_mode : Local")
