from django.db import models
from django.db.models import BooleanField as _BooleanField
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, AbstractBaseUser
# from django.urls import reverse
import django.utils.timezone as timezone
# from django.core.validators import RegexValidator
# from django.template.defaultfilters import slugify
# from datetime import datetime
# import pytz
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class BooleanField(_BooleanField):
    def get_prep_value(self, value):
        if value in (0, '0', 'false', 'False'):
            return False
        elif value in (1, '1', 'true', 'True'):
            return True
        else:
            return super(BooleanField, self).get_prep_value(value)


# AbstractBaseUser中只含有3个field: password, last_login和is_active.
# 如果你对django user model默认的first_name, last_name不满意,
# 或者只想保留默认的密码储存方式, 则可以选择这一方式.
class DataXUserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', max_length=200,
                               verbose_name=_('用户头像'))
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ')
    phone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name=_('手机号'))
    nick_name = models.CharField(max_length=30, verbose_name=_('昵称'))

    # is_lock = models.BooleanField(default=False, verbose_name='是否锁定', choices=((0, '否'), (1, '是')))
    # is_enable = models.BooleanField(default=True, verbose_name='是否启用', choices=((0, '否'), (1, '是')))

    class Meta(AbstractUser.Meta):
        db_table = 'dx_userprofile'
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('用户')
        verbose_name_plural = verbose_name
        ordering = ['-id']

    # class Meta:
    #     db_table = 'datax_userprofile'
    #     verbose_name = '用户'
    #     verbose_name_plural = verbose_name
    #     ordering = ['-id']

    def __str__(self):
        return self.username

    # def create_user(self, username, nickname, password=None):
    #     # create user here
    #     pass
    #
    # def create_superuser(self, username, password):
    #     # create superuser here
    #     pass


class BaseModel(models.Model):
    create_time = models.DateTimeField(_('创建时间'), default=timezone.now)
    create_uid = models.IntegerField(_('创建人ID'), default=123456789, auto_created=True)
    create_username = models.CharField(_('创建人名称'), max_length=30, default='admin', auto_created=True)
    operate_time = models.DateTimeField(_('操作时间'), auto_now=True)
    operate_uid = models.IntegerField(_('操作人ID'), default=123456789, auto_created=True)
    operate_username = models.CharField(_('操作人名称'), max_length=30, default='admin', auto_created=True)

    class Meta:
        abstract = True


# 系统|站点配置
class DataXConfig(BaseModel):
    site_name = models.CharField(_('站点名称'), max_length=50, null=True, blank=True)
    site_desc = models.CharField(_('站点描述'), max_length=150, null=True, blank=True)
    site_author = models.CharField(_('作者'), max_length=100, null=True, blank=True)
    site_company = models.CharField(_('公司'), max_length=100, default=None, blank=True, null=True)
    address = models.CharField(_('显示地址'), max_length=150, default=None, blank=True, null=True)
    telephone = models.CharField(_('电话'), max_length=15)
    email = models.EmailField(_('邮箱'), max_length=50, null=True, blank=True)
    icp = models.CharField(_('备案号'), max_length=256, null=True, blank=True)
    remark = models.CharField(_('备注'), max_length=200, null=True, blank=True)
    qrcode = models.ImageField(_('二维码'), null=True, blank=True, upload_to='sys/%Y/%m')
    is_enable = models.BooleanField(_('是否启用'), default=True)

    class Meta:
        db_table = "dx_config"
        verbose_name = _('站点配置')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.site_name


# 导航菜单管理
class DataXNav(BaseModel):
    code = models.CharField(_('标识'), max_length=20)
    name = models.CharField(_('名称'), max_length=50, blank=True, null=True,)
    url = models.CharField(_('链接'), max_length=200)
    remark = models.CharField(_('描述'), max_length=300, blank=True)
    parent = models.ForeignKey(to='self', default=0, null=True, blank=True, related_name='children',
                               verbose_name=_('父级'), limit_choices_to={'is_delete': False, 'is_root': True},
                               on_delete=models.CASCADE)
    is_root = models.BooleanField(_('是否一级菜单'), default=True)
    is_delete = models.BooleanField(_('是否删除'), default=False)
    sort = models.IntegerField(_('排序'), default=0)
    is_enable = models.BooleanField(_('是否启用'), default=True)

    class Meta:
        db_table = "dx_nav"
        ordering = ['sort', '-create_time']
        verbose_name = _('导航菜单管理')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 作业调度
class DataXJobScheduler(BaseModel):
    """
    """
    name = models.CharField(_('作业名称'), max_length=200)
    # type_code = models.PositiveSmallIntegerField(
    #     _('图片业务类型'), default=0,
    #     choices=(
    #         (1, _('企业文化')),
    #         (2, _('品牌荣誉')),
    #         (3, _('企业资质')),
    #         (4, _('团队风采')),
    #         (5, _('品牌故事')),
    #         (6, _('组织架构'))
    #     )
    # )
    # image_url = models.ImageField(_('图片'), null=True, blank=True, upload_to='company/%Y/%m')
    # about = models.ForeignKey(to='ChfAbout', null=True, blank=True, related_name='about_resource',
    #                           related_query_name='about', on_delete=models.CASCADE, verbose_name=_('品牌介绍'))

    # job_speed_channel = models.SmallIntegerField(_('速度'), default=5)
    # job_error_limit_record = models.SmallIntegerField(_('错误记录条数'), default=5)
    # job_error_limit_percentage = models.FloatField(_('错误记录百分比'), default=0.02)

    sort = models.IntegerField(_('排序'), default=10000)
    is_enable = models.BooleanField(_('是否启用'), default=True)

    class Meta:
        db_table = 'dx_jobscheduler'
        ordering = ['sort', '-create_time']
        verbose_name = _('作业调度')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 作业任务
class DataXTask(BaseModel):
    name = models.CharField(_('任务名称'), max_length=256, )
    from_dbtype = models.CharField(_('来源库类型'), max_length=50, )
    from_hostname = models.CharField(_('来源IP'), max_length=16, )
    from_port = models.SmallIntegerField(_('来源端口'), default=3306, )
    from_username = models.CharField(_('来源用户名'), max_length=50, )
    from_password = models.CharField(_('来源密码'), max_length=50, )
    from_db_name = models.CharField(_('来源库名'), max_length=80, )
    from_table_name = models.CharField(_('来源表名'), max_length=80, )
    from_columns = models.CharField(_('来源列'), default='*', max_length=1000, )
    from_where = models.CharField(_('来源条件'), default='', max_length=1000, )
    from_character = models.CharField(_('来源编码'), default='utf8', max_length=10, )

    to_dbtype = models.CharField(_('目标库类型'), max_length=50, )
    to_hostname = models.CharField(_('目标IP'), max_length=16, )
    to_port = models.SmallIntegerField(_('目标端口'), default=3306, )
    to_username = models.CharField(_('目标用户名'), max_length=50, )
    to_password = models.CharField(_('目标密码'), max_length=50, )
    to_db_name = models.CharField(_('目标库名'), max_length=80, )
    to_table_name = models.CharField(_('目标表名'), max_length=80, )
    to_columns = models.CharField(_('目标列'), default='*', max_length=1000, )
    to_pre_sql = models.CharField(_('前置条件'), default='', max_length=1000, )
    to_post_sql = models.CharField(_('后置条件'), default='', max_length=1000, )
    to_character = models.CharField(_('目标编码'), default='utf8', max_length=10, )
    to_session = models.CharField(_('目标session'), default='', max_length=256)
    to_write_mode = models.CharField(_('目标写入模式'), default='insert', max_length=15)

    task_speed_channel = models.SmallIntegerField(_('速度'), default=5)
    task_error_limit_record = models.SmallIntegerField(_('错误记录条数'), default=5)
    task_error_limit_percentage = models.FloatField(_('错误记录百分比'), default=0.02)

    sort = models.IntegerField(_('排序'), default=0)
    is_enable = models.BooleanField(_('是否启用'), default=True)

    class Meta:
        db_table = 'dx_task'
        ordering = ['-create_time']
        verbose_name = _('作业任务')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # def long_profile(self):
    #     if len(str(self.long_content)) > 50:
    #         return '{}...'.format(str(self.long_content)[0:50])
    #     else:
    #         return str(self.long_content)
    #
    # long_profile.allow_tags = True
    # long_profile.short_description = _('')


