"""
查看API使用统计的管理命令
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from invitation.models import APIUsageStats


class Command(BaseCommand):
    help = '显示API使用统计信息'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='指定日期 (YYYY-MM-DD)，默认为今天',
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['geocode', 'reverse_geocode'],
            help='指定API类型',
        )

    def handle(self, *args, **options):
        target_date = options.get('date')
        api_type = options.get('type')
        
        if target_date:
            from datetime import datetime
            try:
                target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('日期格式错误，请使用 YYYY-MM-DD 格式')
                )
                return
        else:
            target_date = timezone.now().date()
        
        # 查询统计信息
        if api_type:
            # 查询特定类型的统计
            stat = APIUsageStats.get_daily_stats(api_type, target_date)
            if stat:
                self.display_stat(stat)
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'没有找到 {target_date} {api_type} 的统计信息'
                    )
                )
        else:
            # 查询所有类型的统计
            for api_type_choice, _ in APIUsageStats.API_TYPES:
                stat = APIUsageStats.get_daily_stats(api_type_choice, target_date)
                if stat:
                    self.display_stat(stat)
                    self.stdout.write('')  # 空行分隔
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'没有找到 {target_date} {api_type_choice} 的统计信息'
                        )
                    )

    def display_stat(self, stat):
        """显示统计信息"""
        status_color = self.style.SUCCESS if stat.rate_limit_hit else self.style.WARNING
        rate_limit_status = '是' if stat.rate_limit_hit else '否'
        
        self.stdout.write(
            self.style.HTTP_INFO(f'API类型: {stat.api_type}')
        )
        self.stdout.write(f'日期: {stat.date}')
        self.stdout.write(f'调用次数: {stat.call_count}')
        self.stdout.write(f'成功次数: {stat.success_count}')
        self.stdout.write(f'错误次数: {stat.error_count}')
        self.stdout.write(status_color(f'达到速率限制: {rate_limit_status}'))
        self.stdout.write(f'创建时间: {stat.created_at}')
        self.stdout.write(f'更新时间: {stat.updated_at}')