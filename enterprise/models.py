from django.db import models
from myrsa2.models import EncryptionAlgorithm, Enterprise


class TbOfEnt(models.Model):
    """当前企业就一个app"""
    enc_alg = models.ForeignKey(EncryptionAlgorithm, related_name='tbofent',
                                on_delete=models.SET_NULL, null=True, verbose_name='加密算法')
    app_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='app_id')
    app_secret = models.CharField(max_length=100, blank=True, null=True, verbose_name='app_secret')
    plat_pub_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name='平台公钥')
    ent_pub_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name='企业公钥')
    ent_pri_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name='企业私钥')
    enterprise = models.ForeignKey(Enterprise, related_name='tbofent', on_delete=models.CASCADE)
    ent_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='企业名字')

    class Meta:
        db_table = 'table_of_enterprise'
