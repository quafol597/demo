package com.xiaoantimes.commons;

import com.xiaoantimes.commons.api.Sm2Service;

/**
 * Hello world!
 */
public class App {
    public static void main(String[] args) throws Exception{
        // win:   java -cp sm2-1.0-SNAPSHOT.jar;F:/GitSpace/lib/* com.xiaoantimes.commons.App
        // linux: java -cp sm2-1.0-SNAPSHOT.jar:/data/sm2/lib/* com.xiaoantimes.commons.App
        // https://www.cnblogs.com/qixing/p/11457728.html
        System.out.println(Sm2Service.generateKeys());
    }
}
