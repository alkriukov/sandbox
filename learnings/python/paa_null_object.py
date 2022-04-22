import os

# The pattern needs AbstractObject base class and child classes: RealObject and NullObject
# All provide same interface (startJob and stopJob in our case)
class AbstractObject:
    def request():
        pass

class RealObject(AbstractObject):
    def request():
        print('Real proessing')

class NullObject(AbstractObject):
    def request():
        print('Null handling')


# To demonstrate advantages, let's have some real procssing
class AbstractWorker:
    work = ''
    def __init__(self) -> None:
        pass
    def startJob(self):
        pass
    def stopJob(self):
        pass

class RealWorker(AbstractWorker):
    def __init__(self, work) -> None:
        super().__init__()
        self.work = work
    def startJob(self):
        print(' - start, '.join(self.work.split()) + ' - start.')
    def stopJob(self):
        print(' - stop, '.join(self.work.split()) + ' - stop.')

class NullWorker(AbstractWorker):
    def __init__(self) -> None:
        super().__init__()
        self.work = 'Nothing to do'
    def startJob(self):
        print(self.work)
    def stopJob(self):
        print('I was not busy')

# and let's have a factory
def WorkerFactory(input):
    if input == None:
        return NullWorker()
    else:
        return RealWorker(input)

# So the main code doesn\'t care on checking for None
def main():
    works = ['read write', 'run jump', None, None, 'sing']
    workers = []
    for work in works:
        workers.append(WorkerFactory(work))
    
    print('Let all workers do their job')
    for worker in workers:
        worker.startJob()
    print('\ntime to finish')
    for worker in workers:
        worker.stopJob()
    
    print('\nNow let\'s do only real job')
    for realWorker in workers:
        if isinstance(realWorker, RealWorker):
            realWorker.startJob()

if __name__ == '__main__':
    main()
