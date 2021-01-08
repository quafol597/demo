import jpype
import os

"""
基本的开发流程如下：
①、使用jpype开启jvm
②、加载java类
③、调用java方法
④、关闭jvm（不是真正意义上的关闭，卸载之前加载的类）
"""


def get_hex_keys(basedir):

    jarpath = os.path.join(basedir, 'sm2', 'sm2-1.0-SNAPSHOT.jar')
    lib = os.path.join(basedir, "lib")
    a, b, c = [os.path.join(lib, i) for i in os.listdir(lib)]

    jvmpath = jpype.getDefaultJVMPath()

    jpype.startJVM(jvmpath, "-ea", f"-Djava.class.path={jarpath};{a};{b};{c}")
    Sm2Service = jpype.JClass("com.xiaoantimes.commons.api.Sm2Service")
    print(Sm2Service.generateKeys())

    jpype.shutdownJVM()


if __name__ == '__main__':
    get_hex_keys(basedir=r"C:\Users\xiaoan\Desktop\sm2")
