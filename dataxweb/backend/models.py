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
from django.utils.html import format_html

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
    hostname = models.CharField(_('作业机器名称'), max_length=100, default='', null=True, blank=True)
    ip = models.CharField(_('作业机器ip'), max_length=100, default='127.0.0.1', )
    port = models.PositiveSmallIntegerField(_('作业机器端口'), default=9999, )
    deploy_state = models.PositiveSmallIntegerField(
        _('作业部署状态'), default=0,
        choices=(
            (0, _('未部署')),
            (1, _('已部署')),
        )
    )
    state = models.PositiveSmallIntegerField(
        _('作业运行状态'), default=0,
        choices=(
            (0, _('未运行')),
            (1, _('运行中')),
            (2, _('结束')),
            (3, _('异常终止')),
        )
    )
    start_time = models.DateTimeField(_('作业开始时间'), default='', null=True, blank=True, )
    end_time = models.DateTimeField(_('作业结束时间'), default='', null=True, blank=True, )
    duration = models.IntegerField(_('运行时长'), default=0)

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

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='127.0.0.1:9000/admin/123'>查看</a>")

    go_to.short_description = "操作"


# 作业任务
class DataXTask(BaseModel):
    scheduler = models.OneToOneField(
        DataXJobScheduler, null=False,
        related_name='Scheduler',  # 反向查询用(就不_set了：d1.DataXTask.all() -》d1.Scheduler.all())
        on_delete=models.CASCADE,  # 外键,自动关联表的主键 级联删除
        to_field='id', verbose_name=_('作业任务')
    )
    name = models.CharField(_('任务名称'), max_length=256, help_text='此名称用于保存为json模板名称')
    from_dbtype = models.CharField(_('来源库类型'), max_length=50, )
    from_hostname = models.CharField(_('来源IP'), max_length=16, )
    from_port = models.SmallIntegerField(_('来源端口'), default=3306, )
    from_username = models.CharField(_('来源用户名'), max_length=50, )
    from_password = models.CharField(_('来源密码'), max_length=50, )
    from_db_name = models.CharField(_('来源库名'), max_length=80, )
    from_table_name = models.CharField(_('来源表名'), max_length=80, )
    from_columns = models.CharField(_('来源列'), default='*', max_length=1000, null=True, blank=True, )
    from_where = models.CharField(_('来源条件'), default='', max_length=1000, null=True, blank=True, )
    from_character = models.CharField(_('来源编码'), default='utf8', max_length=10, null=True, blank=True, )

    to_dbtype = models.CharField(_('目标库类型'), max_length=50, )
    to_hostname = models.CharField(_('目标IP'), max_length=16, )
    to_port = models.SmallIntegerField(_('目标端口'), default=3306, )
    to_username = models.CharField(_('目标用户名'), max_length=50, )
    to_password = models.CharField(_('目标密码'), max_length=50, )
    to_db_name = models.CharField(_('目标库名'), max_length=80, )
    to_table_name = models.CharField(_('目标表名'), max_length=80, )
    to_columns = models.CharField(_('目标列'), default='*', max_length=1000, null=True, blank=True, )
    to_pre_sql = models.CharField(_('前置条件'), default='', max_length=1000, null=True, blank=True, )
    to_post_sql = models.CharField(_('后置条件'), default='', max_length=1000, null=True, blank=True, )
    to_character = models.CharField(_('目标编码'), default='utf8', max_length=10, null=True, blank=True, )
    to_session = models.CharField(_('目标session'), default='', max_length=256, null=True, blank=True, )
    to_write_mode = models.CharField(_('目标写入模式'), default='insert', max_length=15)

    task_speed_channel = models.SmallIntegerField(_('速度'), default=5, null=True, blank=True, )
    task_error_limit_record = models.SmallIntegerField(_('错误记录条数'), default=5, null=True, blank=True, )
    task_error_limit_percentage = models.FloatField(_('错误记录百分比'), default=0.02, null=True, blank=True, )

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

    # 用format_html()或者format_html_join()或者mark_safe()方法
    def from_address(self):
        # 关键是这句！！！！！请自己调整缩进。
        return format_html(
            '<span style="color: #{};">{}:{}</span>',
            'green',
            self.from_hostname,
            self.from_port,
        )

    def to_address(self):
        # 关键是这句！！！！！请自己调整缩进。
        return format_html(
            '<span style="color: #{};">{}:{}</span>',
            'red',
            self.to_hostname,
            self.to_port,
        )


# 作业任务状态
class DataXTaskStatus(BaseModel):
    """
    """
    task = models.ManyToManyField(
        DataXTask, null=True,
        related_name='Task',  # 反向查询用(就不_set了：d1.DataXTaskStatus_set.all() -》d1.Task.all())
        # through=''
        verbose_name=_('任务状态')
    )
    name = models.CharField(_('任务名称'), max_length=200)
    state = models.PositiveSmallIntegerField(
        _('任务状态'), default=0,
        choices=(
            (0, _('未运行')),
            (1, _('运行中')),
            (2, _('已完成')),
            (3, _('终止')),
        )
    )
    start_time = models.DateTimeField(_('开始时间'), default='', null=True, blank=True, )
    end_time = models.DateTimeField(_('结束时间'), default='', null=True, blank=True, )
    duration = models.IntegerField(_('运行时长'), default=0)

    class Meta:
        db_table = 'dx_taskstatus'
        ordering = ['-create_time']
        verbose_name = _('任务状态')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


