"""测试报告生成器"""
import json
from datetime import datetime
from typing import Dict, List


class TestReport:
    """生成测试执行报告"""
    
    def __init__(self):
        self.results = {
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "tests": []
        }
    
    def add_test_result(self, test_name: str, status: str, duration: float, 
                       error: str = None):
        """添加测试结果"""
        self.results["tests"].append({
            "name": test_name,
            "status": status,
            "duration": duration,
            "error": error
        })
        
        self.results["total"] += 1
        if status == "passed":
            self.results["passed"] += 1
        elif status == "failed":
            self.results["failed"] += 1
        elif status == "skipped":
            self.results["skipped"] += 1
    
    def finalize(self):
        """完成报告"""
        self.results["end_time"] = datetime.now().isoformat()
    
    def save_json(self, filepath: str = "test-results/report.json"):
        """将报告保存为JSON格式"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
    
    def get_summary(self) -> str:
        """获取报告摘要"""
        return f"""
Test Execution Summary
======================
Total Tests: {self.results['total']}
Passed: {self.results['passed']}
Failed: {self.results['failed']}
Skipped: {self.results['skipped']}
Success Rate: {self.results['passed']/max(self.results['total'], 1)*100:.2f}%
        """
