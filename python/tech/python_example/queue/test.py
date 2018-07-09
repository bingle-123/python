# -*- coding:utf-8 -*-

#IO密集型任务
#多个进程同时下载多个网页
#利用Queue+多进程
#由于是IO密集型,所以同样可以利用threading模块

import multiprocessing

def main():
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    cpu_count = multiprocessing.cpu_count()  #进程数目==CPU核数目

    create_process(tasks, results, cpu_count)   #主进程马上创建一系列进程,但是由于阻塞队列tasks开始为空,副进程全部被阻塞
    add_tasks(tasks)  #开始往tasks中添加任务
    parse(tasks, results)  #最后主进程等待其他线程处理完成结果


def create_process(tasks, results, cpu_count):
    for _ in range(cpu_count):
        p = multiprocessing.Process(target=_worker, args=(tasks, results)) #根据_worker创建对应的进程
        p.daemon = True  #让所有进程可以随主进程结束而结束
        p.start() #启动

def _worker(tasks, results):
    while True:   #因为前面所有线程都设置了daemon=True,故不会无限循环
        try:
            task = tasks.get()   #如果tasks中没有任务,则阻塞
	    name=multiprocessing.current_process().name
	    print task,name
	
            result = task
            results.put(result)   #some exceptions do not handled
        finally:
            tasks.task_done()

def add_tasks(tasks):
    for url in range(10):  #get_urls() return a urls_list
        tasks.put(url)

def parse(tasks, results):
    try: 
        tasks.join()
    except KeyboardInterrupt as err:
        print "Tasks has been stopped!"
        print err

#    while not results.empty():
#	print results.get()


if __name__ == '__main__':
    main()


