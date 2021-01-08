## 一、apiutils包文档说明: 

> apiutils包可以实现, 自动为用户请求添加签名, 访问小安平台并获取响应数据, 验证对方签名.



1. 构建apiutils对象

   ```python
   # appid = "您的appid" (int, str类型皆可)
   # plat_pub_key = "小安发给您的公钥" (包括 BEGIN 和 END 行)
   # app_priv_key = "您的私钥" (包括 BEGIN 和 END 行)
   apiutils = APIUtils(appid=appid,
                       plat_pub_key_string=plat_pub_key,  
                       app_private_key_string=app_priv_key, 
                       sign_type='RSA2')
   
   # 亦可通过: plat_pub_key_path和app_private_key_path参数导入密钥文件绝对路径。
   ```

2. 调用接口

   ```python
   # 以api_apiutls_books接口为例: 获取图书列表.
   
   content = apiutils.api_apiutils_books(subject="...")
   """
   self.api_apiutils_books()
   	<1> 包装用户原始信息, 并自动添加签名.
   	<2> 向小安发送请求,
   	<3> 返回content字典, PS:
   		content = {
   			"result": ...,  # 小安响应数据
   			"signature_x": ...  # 小安签名, 用于self.verify函数验签
   		}
   """
   ```

3. 验签

   ```python
   result = content['result']
   signature = content['signature_x']
   
   apiutils.verify(result, signature)  
   """
   self.verify(dict, str) -> bool:
   	
   	return True  # 验签通过, 得到未经篡改的result.
   	return False  # 验签失败, 请重新发送请求.
   
   """
   ```
## 二、apiutils接口文档
   
   
   
   
   
   
   
   

   

   