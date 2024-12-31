# 定义一个动物基类，用于描述一般动物的行为
class Animal:
    def sound(self):
        raise NotImplementedError("请在子类中实现 sound 方法")


# 继承 Animal 的子类，分别实现各自的叫声
class Dog(Animal):
    def sound(self):
        return "汪汪"


class Cat(Animal):
    def sound(self):
        return "喵喵"


def make_sound(animal: Animal):
    print(animal.sound())


# 通过传入不同的对象观察多态效果
dog = Dog()
cat = Cat()
make_sound(dog)  # 输出: 汪汪
make_sound(cat)  # 输出: 喵喵