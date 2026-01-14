"""
清理过期地理编码缓存的管理命令
"""

from django.core.management.base import BaseCommand
from invitation.models import GeocodingCache


class Command(BaseCommand):
    help = '清理过期的地理编码缓存'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅显示将要删除的条目数量，不实际删除',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        if dry_run:
            # 仅计算将要删除的数量
            from django.utils import timezone
            expired_count = GeocodingCache.objects.filter(
                expires_at__lt=timezone.now()
            ).count()
            self.stdout.write(
                self.style.WARNING(
                    f'将有 {expired_count} 条过期缓存条目被删除（--dry-run模式）'
                )
            )
        else:
            # 实际删除过期缓存
            deleted_count = GeocodingCache.cleanup_expired_cache()
            self.stdout.write(
                self.style.SUCCESS(
                    f'成功清理了 {deleted_count} 条过期的地理编码缓存'
                )
            )