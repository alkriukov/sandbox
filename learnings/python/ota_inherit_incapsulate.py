class Engine:
    __volume = 0
    __power = 0
    __nm = 0
    __fuel = ''
    def __init__(self, volume, power, nm, fuel):
        self.__volume = volume
        self.__power = power
        self.__nm = nm
        self.__fuel = fuel
    @property
    def volume(self):
        return self.__volume
    @property
    def power(self):
        return self.__power
    @property
    def nm(self):
        return self.__nm
    @property
    def fuel(self):
        return self.__fuel


class TurboEngine(Engine):
    __nm = 0
    @property
    def nm(self):
        print(super.nm)
        return self.__nm

some_engine = Engine(2000, 150, 200, 'ai-92')
print(some_engine.volume)

turbo_engine = TurboEngine(2000, 200, 300, 'ai-95')
print(turbo_engine.nm)
