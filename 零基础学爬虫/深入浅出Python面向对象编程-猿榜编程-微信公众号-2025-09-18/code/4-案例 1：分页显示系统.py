class Paginator:
    def __init__(self,current_page,per_page=10):
        try:
            self.current_page=int(current_page)
        except ValueError:
            self.current_page=1
        if self.current_page<1:
            self.current_page=1
        self.per_page=per_page

    def start_index(self):
        # 返回当前页面的起始索引（从0开始计算）
        return (self.current_page-1)*self.per_page

    def end_index(self):
        # 返回当前页面的结束索引
        return self.current_page*self.per_page

if __name__ == '__main__':
    # 构造测试数据，并模拟分页显示
    items=[f"Item {i}" for i in range(1,101)]
    page_number=input("请输入页码数：")
    page=Paginator(page_number,per_page=10)
    print("当前页数据：")
    for item in items[page.start_index():page.end_index()]:
        print(item)