from backend import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.contenttypes.models import ContentType

# Register your models here.
admin.site.index_title = _('欢迎使用DataX管理系统')
admin.site.site_title = _('DataX管理系统')
admin.site.site_header = _('DataX管理系统')


# 编写可用于整个admin站点的action
# admin.site.add_action(export_selected_objects)

# 禁用全站级别的 acitons
# 禁用内置的删除方法
# admin.site.disable_action('delete_selected')

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
    list_display = ('id', 'name', 'hostname', 'ip', 'port', 'deploy_state', 'state', 'start_time',
                    'end_time', 'duration', 'sort', 'is_enable')
    list_display_links = ('id', 'name', )
    list_editable = ('is_enable', 'hostname', 'ip', 'port', )
    list_filter = (IsEnableFilter, )
    list_per_page = 10
    search_fields = ('name', 'hostname', 'ip', 'port', )
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username',)

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

    # class Media:
    #     js = (
    #         # '/static/plugins/kindeditor-4.1.10/kindeditor-all-min.js',
    #         '/static/plugins/kindeditor-4.1.10/kindeditor.js',
    #         '/static/plugins/kindeditor-4.1.10/lang/zh_CN.js',
    #         '/static/plugins/kindeditor-4.1.10/config.js',
    #     )

    actions = ['view_job_json', 'view_job_task', 'deploy_job', 'start_job', 'stop_job', 'view_job_log', ]

    def view_job_json(self, request, queryset):
        pass

    view_job_json.short_description = '查看作业json'

    def deploy_job(self, request, queryset):
        # 操作完成后的提示信息
        self.message_user(request, '作业部署成功！')

        # response = HttpResponse(content_type="application/json")
        # serializers.serialize("json", queryset, stream=response)
        # return response

        # 获得被打钩的checkbox对应的对象
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        # 获取对应的模型
        ct = ContentType.objects.get_for_model(queryset.model)
        # 构造访问的url，使用GET方法，跳转到相应的页面
        return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

    deploy_job.short_description = '部署作业'

    def view_job_task(self, request, queryset):
        pass

    view_job_task.short_description = '查看作业任务'

    def start_job(self, request, queryset):
        # 操作完成后的提示信息
        self.message_user(request, '作业已启动！')

    start_job.short_description = '启动作业'

    def stop_job(self, request, queryset):
        # 操作完成后的提示信息
        self.message_user(request, '作业已停止！')

    stop_job.short_description = '停止作业'

    def view_job_log(self, request, queryset):
        pass

    view_job_log.short_description = '查看作业日志'


# 作业任务
@admin.register(models.DataXTask)
class DataXTaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'from_dbtype', 'from_hostname', 'from_port', 'from_username', 'from_password',
                    'from_db_name', 'from_table_name', 'from_columns', 'from_where', 'from_character',
                    'to_dbtype', 'to_hostname', 'to_port', 'to_username', 'to_password',
                    'to_db_name', 'to_table_name', 'to_columns', 'to_pre_sql', 'to_post_sql', 'to_character',
                    'to_session', 'to_write_mode', 'task_speed_channel', 'task_error_limit_record',
                    'task_error_limit_percentage', 'sort', 'is_enable')
    list_display_links = ('id', 'name',)
    list_editable = ('is_enable',)
    list_filter = (IsEnableFilter, )
    list_per_page = 10
    # list_max_show_all = 200
    # paginator = Paginator
    preserve_filters = True
    # Action选项都是在页面上方显示
    # actions_on_top = True
    # Action选项都是在页面下方显示
    # actions_on_bottom = False
    # 是否显示选择个数
    # actions_selection_counter = True
    save_on_top = True
    # save_as = False
    # save_as_continue = False
    search_fields = (
        'name', 'from_dbtype', 'from_hostname', 'from_port', 'from_username',
        'from_db_name', 'from_table_name', 'from_columns', 'from_where',
        'to_dbtype', 'to_hostname', 'to_port', 'to_username',
        'to_db_name', 'to_table_name', 'to_columns', 'to_pre_sql', 'to_post_sql',
    )
    fieldsets = (
        ('来源', {
            # 'classes': ('collapse', ),
            'fields': [
                'from_dbtype', 'from_hostname', 'from_port', 'from_username', 'from_password',
                'from_db_name', 'from_table_name', 'from_columns', 'from_where', 'from_character',
            ],
        }),
        ('目标', {
            # 'classes': ('collapse', 'wide', 'extrapretty'),
            'fields': [
                'to_dbtype', 'to_hostname', 'to_port', 'to_username', 'to_password',
                'to_db_name', 'to_table_name', 'to_columns', 'to_pre_sql', 'to_post_sql', 'to_character',
                'to_session', 'to_write_mode',
            ],
        }),
        ('其他', {
            'fields': [
                'task_speed_channel', 'task_error_limit_record',
                'task_error_limit_percentage', 'sort', 'is_enable'
            ],
        }),
    )
    # date_hierarchy = 'create_time'  # 详细时间分层筛选

    # 只读字段
    # readonly_fields = (, )

    # # 添加数据模板页
    # add_form_template = None
    # # 修改数据的模板页
    # change_form_template = None
    # # 修改多条数据的模板页
    # change_list_template = None
    # # 删除确认信息模板页
    # delete_confirmation_template = None
    # # 删除关联数据的确认页
    # delete_selected_confirmation_template = None
    # # 修改历史的模板页
    # object_history_template = None

    # 弹出框模板页
    popup_response_template = None

    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username',)
    actions = ['view_task_json', 'start_task', 'stop_task', 'view_task_log', 'export_as_json', ]
    # 排序
    # ordering = ('-id',)
    # def get_ordering(self, request):
    #     return ['-id', ]

    def save_model(self, request, obj, form, change):
        print('*' * 100)
        print(obj.name, obj.from_dbtype, obj.from_hostname, obj.from_port, obj.from_username, obj.from_password)
        print(obj.name, obj.to_dbtype, obj.to_hostname, obj.to_port, obj.to_username, obj.to_password)
        print('*' * 100)

        if change:
            pass
            # 修改
            # 修改对应的json模板文件
        else:
            pass
            # 新增
            # 新增对应的json模板文件

        super(DataXTaskAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # 停止任务
        super(DataXTaskAdmin, self).delete_model(request, obj)

    def view_task_json(self, request, queryset):
        pass

    view_task_json.short_description = '查看任务json'

    # 定制Action行为具体方法
    def start_task(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))
        print(request, queryset)
        # queryset.update(status='published')
        # 操作完成后的提示信息
        self.message_user(request, '任务已启动！')

    start_task.short_description = "启动任务"

    def stop_task(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))
        print(request, queryset)
        # queryset.update(status='published')
        # 操作完成后的提示信息
        self.message_user(request, '任务已停止！')

    stop_task.short_description = "停止任务"

    def view_task_log(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))
        print(request, queryset)
        # queryset.update(status='published')
        # 操作完成后的提示信息
        # self.message_user(request, '任务已停止！')

    view_task_log.short_description = "查看任务日志"

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response)
        return response

    export_as_json.short_description = '导出json'

    # def export_selected_objects(self, request, queryset):
    #     # 获得被打钩的checkbox对应的对象
    #     selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    #     # 获取对应的模型
    #     ct = ContentType.objects.get_for_model(queryset.model)
    #     # 构造访问的url，使用GET方法，跳转到相应的页面
    #     return HttpResponseRedirect("/export/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))


@admin.register(models.DataXTaskStatus)
class DataXTaskStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state', 'start_time', 'end_time', 'duration')
    list_display_links = ('id', 'name')
    # list_filter = ()
    list_per_page = 10
    search_fields = ('task', 'name', )
    exclude = ('create_uid', 'create_username', 'create_time', 'operate_uid', 'operate_username')

    # 屏蔽增加功能按钮
    def has_add_permission(self, request):
        return False

    # 屏蔽删除功能按钮
    def has_delete_permission(self, request, obj=None):
        return False

    # 屏蔽修改功能按钮
    def has_change_permission(self, request, obj=None):
        return False
