from django.db import models


class Enterprise(models.Model):
    """企业信息"""
    ent_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='企业名字')

    class Meta:
        db_table = 'enterprise'

    def __str__(self):
        return self.ent_name


class EncryptionAlgorithm(models.Model):
    """加密码表"""
    enc_alg = models.CharField(max_length=10, verbose_name='算法名')

    class Meta:
        db_table = 'tb_encrypt_algorithm'


class App(models.Model):
    """app信息, 及其关联的企业"""
    enc_alg = models.ForeignKey(EncryptionAlgorithm, related_name='app',
                                on_delete=models.SET_NULL, null=True, verbose_name='加密算法')
    app_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='app_id')
    app_secret = models.CharField(max_length=100, blank=True, null=True, verbose_name='app_secret')
    plat_pri_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name='平台私钥')
    plat_pub_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name='平台公钥')
    ent_pub_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name='企业公钥')
    enterprise = models.ForeignKey(Enterprise, related_name='app', on_delete=models.CASCADE)
    ent_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='企业名字')

    class Meta:
        db_table = 'app'
