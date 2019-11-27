from backend import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry
from django.utils.translation import ugettext_lazy as _

# Register your models here.
admin.site.index_title = _('欢迎使用DataX管理系统')
admin.site.site_title = _('DataX管理系统')
admin.site.site_header = _('DataX管理系统')


# 是否启用过滤
class IsEnableFilter(SimpleListFilter):
    title = '是否启用'
    parameter_name = 'is_enable'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_enable=True)
        elif self.value() == '0':
            return queryset.filter(is_enable=False)
        else:
            return queryset.filter()


# 是否领取
class IsGetFilter(SimpleListFilter):
    title = '是否领取'
    parameter_name = 'is_get'

    def lookups(self, request, model_admin):
        return [(1, '已领取'), (0, '未领取')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_get=True)
        elif self.value() == '0':
            return queryset.filter(is_get=False)
        else:
            return queryset.filter()


# 是否已通知
class IsInformFilter(SimpleListFilter):
    title = '是否通知'
    parameter_name = 'is_inform'

    def lookups(self, request, model_admin):
        return [(1, '已通知'), (0, '未通知')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_inform=True)
        elif self.value() == '0':
            return queryset.filter(is_inform=False)
        else:
            return queryset.filter()


# 是否推荐
class IsRecommandFilter(SimpleListFilter):
    title = '是否推荐'
    parameter_name = 'is_recommand'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_recommand=True)
        elif self.value() == '0':
            return queryset.filter(is_recommand=False)
        else:
            return queryset.filter()


# 超级用户状态
class IsSuperUserFilter(SimpleListFilter):
    title = '超级用户状态'
    parameter_name = 'is_superuser'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_superuser=True)
        elif self.value() == '0':
            return queryset.filter(is_superuser=False)
        else:
            return queryset.filter()


# 超级用户状态
class IsActiveFilter(SimpleListFilter):
    title = '是否有效'
    parameter_name = 'is_superuser'

    def lookups(self, request, model_admin):
        return [(1, '是'), (0, '否')]

    def queryset(self, request, queryset):
        # pdb.set_trace()
        if self.value() == '1':
            return queryset.filter(is_active=True)
        elif self.value() == '0':
            return queryset.filter(is_active=False)
        else:
            return queryset.filter()


# admin here
# 管理员
@admin.register(models.DataXUserProfile)
class DataXUserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'nick_name', 'first_name', 'last_name', 'qq', 'phone',
                    'is_superuser', 'is_active', )
    list_display_links = ('username', )
    list_editable = ('nick_name', 'qq', 'phone', 'is_superuser', 'is_active', )
    list_per_page = 30
    list_filter = (IsSuperUserFilter, IsActiveFilter, 'groups')
    search_fields = ('username', 'nick_name', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username', )


# 系统配置
@admin.register(models.DataXConfig)
class DataXConfigAdmin(admin.ModelAdmin):
    # def get_queryset(self, request):
    #     """使当前登录的用户只能看到自己负责的记录"""
    #     qs = super(SysConfigAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #
    #     return qs.filter(user=models.ChfUserProfile.objects.filter(username=request.user))

    # def get_readonly_fields(self, request, obj=None):
    #     """  重新定义此函数，限制普通用户所能修改的字段  """
    #     if request.user.is_superuser:
    #         self.readonly_fields = []
    #
    #     return self.readonly_fields
    #
    # readonly_fields = ('id', 'code', 'name', 'url', 'parent', 'sort', 'is_root', 'is_enable', 'is_delete')

    list_display = ('id', 'site_name', 'site_desc', 'site_author', 'site_company', 'address', 'telephone', 'email',
                    'icp', 'is_enable', 'qrcode')
    list_display_links = ('id', 'site_name', )
    # list_editable = ('telephone', 'is_enable', 'icp')
    list_filter = (IsEnableFilter, )
    list_per_page = 10
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username', )
    search_fields = ('site_name', 'site_author', 'site_company', 'address', 'telephone', 'email', 'icp', )


# 导航菜单管理
@admin.register(models.DataXNav)
class DataXNavAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'url', 'parent', 'sort', 'is_root', 'is_enable', 'is_delete')
    list_display_links = ('id', 'name', 'url', )
    list_editable = ('code', 'sort', 'is_enable', )
    list_filter = (IsEnableFilter, )
    list_per_page = 30
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username', )
    search_fields = ('name', 'en_name', 'url', )


# 用户日志
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'object_repr', 'action_flag', 'user', 'change_message', )

    # 屏蔽增加功能按钮
    def has_add_permission(self, request):
        return False

    # 屏蔽删除功能按钮
    def has_delete_permission(self, request, obj=None):
        return False

    # 屏蔽修改功能按钮
    def has_change_permission(self, request, obj=None):
        return False


# 作业调度
@admin.register(models.DataXJobScheduler)
class DataXJobSchedulerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sort', 'is_enable')
    list_display_links = ('id', 'name',)
    list_editable = ('is_enable',)
    list_filter = (IsEnableFilter, )
    list_per_page = 10
    search_fields = ('name',)
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username',)

    # fieldsets = (
    #     ('基本设置', {
    #         'fields': ('name', 'brief', 'product_type', )
    #     }),
    #     ('高级设置', {
    #         'classes': ('collapse', ),
    #         'fields': ('read_count', 'content', 'cover_image_url', 'sort', 'is_recommand')
    #     }),
    # )

    # list_max_show_all =
    # list_per_page =
    # list_select_related =
    # change_list_template =
    # sortable_by =
    # '''每页显示条目数'''
    # list_per_page = 10
    # 按日期筛选
    # date_hierarchy = 'create_time'
    # 按创建日期排序
    # ordering = ('-create_time',)
    # prepopulated_fields = {'slug': ('name',)}

    class Media:
        js = (
            # '/static/plugins/kindeditor-4.1.10/kindeditor-all-min.js',
            '/static/plugins/kindeditor-4.1.10/kindeditor.js',
            '/static/plugins/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/plugins/kindeditor-4.1.10/config.js',
        )


# 作业任务
@admin.register(models.DataXTask)
class DataXTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'from_dbtype', 'from_hostname', 'from_port', 'from_username', 'from_password',
                    'from_db_name', 'from_table_name', 'from_columns', 'from_where', 'from_character',
                    'to_dbtype', 'to_hostname', 'to_port', 'to_username', 'to_password',
                    'to_db_name', 'to_table_name', 'to_columns', 'to_pre_sql', 'to_post_sql', 'from_character',
                    'to_session', 'to_write_mode', 'task_speed_channel', 'task_error_limit_record',
                    'task_error_limit_percentage', 'sort', 'is_enable')
    list_display_links = ('id', 'name',)
    list_editable = ('is_enable',)
    list_filter = (IsEnableFilter, )
    list_per_page = 10
    search_fields = ('name',)
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username',)

    # fieldsets = (
    #     ('基本设置', {
    #         'fields': ('name', 'brief', 'product_type', )
    #     }),
    #     ('高级设置', {
    #         'classes': ('collapse', ),
    #         'fields': ('read_count', 'content', 'cover_image_url', 'sort', 'is_recommand')
    #     }),
    # )

    # list_max_show_all =
    # list_per_page =
    # list_select_related =
    # change_list_template =
    # sortable_by =
    # '''每页显示条目数'''
    # list_per_page = 10
    # 按日期筛选
    # date_hierarchy = 'create_time'
    # 按创建日期排序
    # ordering = ('-create_time',)
    # prepopulated_fields = {'slug': ('name',)}

    class Media:
        js = (
            # '/static/plugins/kindeditor-4.1.10/kindeditor-all-min.js',
            '/static/plugins/kindeditor-4.1.10/kindeditor.js',
            '/static/plugins/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/plugins/kindeditor-4.1.10/config.js',
        )


