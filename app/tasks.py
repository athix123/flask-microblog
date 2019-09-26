import time
from rq import get_current_job

def example(seconds):
	job = get_current_job()
	print('Starting task')
	for x in range(seconds):
		job.meta['progress'] = 100.0 * x / seconds
		job.save_meta()
		print(x)
		time.sleep(1)
	job.meta['progress'] = 100
	job.save_meta()
	print('Task Completed')