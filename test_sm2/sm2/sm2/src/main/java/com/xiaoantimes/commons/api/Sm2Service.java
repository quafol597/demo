package com.xiaoantimes.commons.api;

import com.alibaba.fastjson.JSON;
import com.xiaoantimes.commons.conf.AppConstant;
import org.apache.commons.codec.binary.Hex;
import org.bouncycastle.jcajce.provider.asymmetric.ec.BCECPrivateKey;
import org.bouncycastle.jcajce.provider.asymmetric.ec.BCECPublicKey;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.SecureRandom;
import java.security.spec.ECGenParameterSpec;
import java.util.HashMap;

/**
 * SM2国密算法服务(python使用)
 *
 * @author chunge
 * @version 1.0
 * @date 2020/10/19
 * @link https://blog.csdn.net/RisenMyth/article/details/107212156
 */
public class Sm2Service {

    /**
     * 生成国密SM2 公私密钥
     * <pre>
     *     私钥: "00" + 私钥(64+2, 66位, 开头增加"00")
     *     公钥: 未压缩密钥 (130-2,128位, 去除标识"04")
     * </pre>
     *
     * @return 国密SM2 公私密钥
     */
    public static String generateKeys() {
        HashMap<String, String> resultMap = new HashMap<>(2);
        try {
            BouncyCastleProvider provider = new BouncyCastleProvider();
            // 获取椭圆曲线相关生成参数规格
            ECGenParameterSpec genParameterSpec = new ECGenParameterSpec("sm2p256v1");
            // 获取一个椭圆曲线类型的密钥对生成器
            KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("EC", provider);
            // 使用SM2的算法区域初始化密钥生成器
            keyPairGenerator.initialize(genParameterSpec, new SecureRandom());

            // 生成密钥对
            KeyPair keyPair = keyPairGenerator.generateKeyPair();
            BCECPrivateKey privateKey = (BCECPrivateKey) keyPair.getPrivate();
            BCECPublicKey publicKey = (BCECPublicKey) keyPair.getPublic();

            // 拿到32字节的私钥HEX privateKey.getD().toString(16)
            String priKey = AppConstant.PRIVATE_KEY_PREFIX + privateKey.getD().toString(16);

            // true  代表压缩密钥，以02、03开头，长度为33字节 Hex.encode(publicKey.getQ().getEncoded(true))
            // false 代表未压缩，以04开头，长度为65字节       Hex.encode(publicKey.getQ().getEncoded(false))
            String pubKey = new String(Hex.encodeHex(publicKey.getQ().getEncoded(false))).substring(2);
            resultMap.put("code", String.valueOf(AppConstant.SUCCESS_CODE));
            resultMap.put("publicKey", pubKey);
            resultMap.put("privateKey", priKey);
        } catch (Exception e) {
            e.printStackTrace();
            resultMap.put("code", String.valueOf(AppConstant.ERROR_CODE));
        }
        return JSON.toJSONString(resultMap);
    }
}