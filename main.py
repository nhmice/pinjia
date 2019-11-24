'''
https://github.com/qinst64/pinjia
说明: 这里实现一种可行的计算方法, 并非为代码质量/速度优化
'''
import datetime
from datetime import datetime, timedelta
from chinaholiday import ChinaHoliday  # https://github.com/qinst64/chinaholiday


class Leave(ChinaHoliday):
    def __init__(self, date_range):
        self.date_range = date_range
        # 获取所有日期
        date_range = [datetime.strptime(d, '%Y%m%d').date()
                      for d in date_range]
        self.all_dates = [
            date_range[0] + timedelta(days=n) for n in range((date_range[-1] - date_range[0]).days)]
        #
        super().__init__()

    def _search(self, n):
        '''
        根据请假天数n搜索拼假
        显然, 我们只关心拼出的假期天数>n+2(2天为周末)
        返回: 3维list, 维度依次为: 拼出m天假期, 假期, 假期的日期
        '''
        #
        temp = []
        for date in self.all_dates:
            # 从date开始搜索
            p_date = date  # 指向日期的指针
            new_holidays = []  # 凑成的假期
            n_used = 0  # 已请假的天数
            # 凑假期
            while n_used < n:
                new_holidays.append(p_date)
                if not self.is_holiday(p_date):
                    n_used += 1
                p_date += timedelta(days=1)
            # 如果之后是假期也加上
            while self.is_holiday(p_date):
                new_holidays.append(p_date)
                p_date += timedelta(days=1)
            if len(new_holidays) > n + 2:
                temp.append(new_holidays)
        # 分组整理
        all_m = list(set(len(r) for r in temp))
        all_m.sort(reverse=True)
        return [[r for r in temp if len(r) == m] for m in all_m]

    def display(self, n):
        '''
        n: 最多请假n天
        打印为markdown格式
        '''
        for n in range(1, n+1):
            print("### 请{}天假".format(n))
            for gp in leave._search(n):
                print("  - 拼出{}天假期".format(len(gp[0])))
                for dates in gp:
                    infos = [leave.get_info(date) for date in dates]
                    names = set(info['holiday_name']
                                for info in infos if info['is_holiday'])
                    highlight = "__" if len(names) > 1 else ""
                    start, end = [d.strftime("%Y%m%d")
                                  for d in [dates[0], dates[-1]]]
                    dates_leave = [info['day'].strftime(
                        "%Y%m%d") for info in infos if not info['is_holiday']]
                    print(
                        f"    - {highlight}{start}至{end}, 拼{'+'.join(names)}, 请假: {'、'.join(dates_leave)}{highlight}")
            print("")


if __name__ == '__main__':
    # 例寻找2020年假期, 最多请假5天, 根据情况调整下边界情况
    date_range = ["201901225", "20201231"]
    leave = Leave(date_range)
    leave.display(4)
