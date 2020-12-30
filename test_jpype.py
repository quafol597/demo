import jpype
import os

"""
基本的开发流程如下：
①、使用jpype开启jvm
②、加载java类
③、调用java方法
④、关闭jvm（不是真正意义上的关闭，卸载之前加载的类）
"""

try:
    jarpath = "/home/zhiyuan/projects/demo/test_java/sm2/sm2/sm2-1.0-SNAPSHOT.jar"
    libpath = '/home/zhiyuan/projects/demo/test_java/sm2/lib/*'
    jvmpath = jpype.getDefaultJVMPath()
    # jpype.startJVM(jvmpath, "-ea", "-Djava.class.path=%s:%s" % (jarpath, libpath))
    jpype.startJVM()

    sm2 = jpype.JClass("com.xiaoantimes.commons.App")

    sm2_json = sm2()
    # TypeError: No matching overloads found for com.xiaoantimes.commons.App.main(), options are:
    # 	public static void com.xiaoantimes.commons.App.main(java.lang.String[]) throws java.lang.Exception
    print(sm2_json)

finally:
    jpype.shutdownJVM()

