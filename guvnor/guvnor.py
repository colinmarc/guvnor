from greenlet import greenlet, getcurrent
import pyuv
import signal

class Watcher(object):
	def __init__(self, greenlet=None):
		if not greenlet:
			greenlet = getcurrent()
		self.greenlet = greenlet
	
	def __call__(self, *args, **kwargs):
		self.greenlet.switch(*args, **kwargs)
	
class Job(object):
	def __init__(self, func=None, *args, **kwargs):
		self.greenlet = greenlet(self.run, parent=guvnor.greenlet)
		self.func = func
		self.args = args
		self.kwargs = kwargs

	def run(self):
		self.func(*self.args, **self.kwargs)
	
	def join(self):
		guvnor.ready_jobs.append(self)
		guvnor.switch()

class Guvnor(object):
	def __new__(cls, *p, **k):
		if not '_instance' in cls.__dict__:
			cls._instance = object.__new__(cls)
		return cls._instance

	def __init__(self):
		self.loop = pyuv.Loop()
		self.greenlet = greenlet(self._run)

		self.dns = pyuv.dns.DNSResolver(self.loop)

		#TODO: benchmark idle vs prepare vs check (depth first vs breadth first)
		self.prepare_handler = pyuv.Idle(self.loop)
		self.prepare_handler.start(self._prepare)

		self.ready_jobs = []
		self.running_jobs = []

	def _run(self):
		self.loop.run()

	def _prepare(self, handler):
		for job in self.ready_jobs:
			job.greenlet.switch()

			if not job.greenlet.dead:
				self.running_jobs.append(job)

		for job in self.running_jobs:
			if job.greenlet.dead:
				self.running_jobs.remove(job)

		self.ready_jobs = []
		if not self.running_jobs:
			main.switch()

	def switch(self):
		self.greenlet.switch()
		
guvnor = Guvnor()
main = getcurrent()

def sleep(secs):
	watcher = Watcher()
	timer = pyuv.Timer(guvnor.loop)
	timer.start(watcher, float(secs), 0)
	guvnor.switch()
	timer.stop()
	timer.close()

def spawn(func, *args, **kwargs):
	return Job(func, *args, **kwargs)

def joinall(jobs):
	guvnor.ready_jobs.extend(jobs)
	guvnor.switch()


if __name__ == '__main__':
	from random import randint
	def dowork(job):
		secs = randint(1, 500) / 100.0
		sleep(secs)
		#print('{0} done! {1} secs'.format(job, secs))

	#job = spawn(dowork, 'stuff')
	#job.join()
	
	print('timing 10000 jobs')
	
	from timeit import Timer
	t = Timer("joinall([spawn(dowork, j) for j in range(10000)])", "from __main__ import spawn, joinall, dowork")
	print(t.timeit(1))

	print('done!')
