# ======================= 配置Django环境: 方法一 ===============================
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
# django.setup()
# ============================================================================

# ======================= 配置Django环境: 方法二 ===============================
from django.conf import settings
settings.configure(
    USE_TZ=True  # 必须大写
)
# ============================================================================


import datetime
from django.utils import timezone
now1 = datetime.datetime.utcnow()
print(type(now1), now1, now1.tzinfo)

now2 = timezone.now()
print(type(now2), now2, now2.tzinfo)

