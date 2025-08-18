import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

plt.style.use("petroff10")  # 或其他可用样式
# print(plt.style.available)

plt.rcParams['font.family'] = 'SimHei'

# 解析函数
def parse_salary(salary_str):
    months = 0
    if "·" in salary_str:
        salary_range, months = salary_str.split("·")
        months = int(months.replace("薪", ""))
    else:
        salary_range = salary_str
        months = 12  # 默认12薪

    low, high = salary_range.split("-")
    low = int(low.replace("K", "")) * months
    high = int(high.replace("K", "")) * months
    return low, high

def gen_box_plot(data, filename: str):
    # 解析数据
    parsed_data = {industry: [sum(parse_salary(salary)) / 24 for salary in salaries] for industry, salaries in data.items()}

    # 准备绘图数据
    industries = list(parsed_data.keys())
    salaries = [parsed_data[industry] for industry in industries]

    # 绘制箱型图
    plt.figure(figsize=(10, 6))
    plt.boxplot(salaries, labels=industries)
    plt.title("行业薪资箱型图")
    plt.ylabel("月薪（K）")
    plt.grid(True)
    plt.savefig(filename, dpi=720, bbox_inches="tight", transparent=True)
    return filename

def draw_pie_chart(data: dict, filename, explode=None, autopct="%1.1f%%"):
    """
    绘制并保存饼图（自动适应数据量的低饱和度配色）

    Args:
        data (dict): 数据字典，格式为 {'类别1': 值1, '类别2': 值2, ...}
        title (str): 图表标题
        filename (str): 保存的文件名（需包含.png后缀）
        explode (list, optional): 突出显示某部分的偏移量. Defaults to None.
        autopct (str, optional): 百分比显示格式. Defaults to '%1.1f%%'.
    """
    # 设置中文字体和样式
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    # # plt.style.use('seaborn')
    # plt.style.use("ggplot")  # 或其他可用样式

    # 动态生成低饱和色系
    def generate_muted_colors(n):
        """生成指定数量的低饱和度颜色"""
        base_colors = [
            "#6E9ED1",
            "#A0CBE8",
            "#F28E2B",
            "#FFBE7D",
            "#59A14F",
            "#8CD17D",
            "#B6992D",
            "#F1CE63",
            "#499894",
            "#86BCB6",
            "#E15759",
            "#FF9D9A",
            "#79706E",
            "#BAB0AC",
            "#D37295",
            "#FABFD2",
            "#B07AA1",
            "#D4A6C8",
            "#9D7660",
            "#D7B5A6",
        ]

        # 如果需求颜色少于基础色数量，直接取用
        if n <= len(base_colors):
            return base_colors[:n]

        # 如果需要更多颜色，通过调整饱和度/亮度生成
        colors = []
        for i in range(n):
            hue = i / n  # 在色相环上均匀分布
            saturation = 0.4 + 0.2 * (i % 3)  # 饱和度在0.4-0.6之间波动
            lightness = 0.6 + 0.15 * (i % 2)  # 亮度在0.6-0.75之间波动
            rgb = mcolors.hsv_to_rgb([hue, saturation, lightness])
            colors.append(mcolors.to_hex(rgb))
        return colors

    # 准备数据
    labels = list(data.keys())
    sizes = list(data.values())
    n_categories = len(data)

    # 自动生成颜色
    colors = generate_muted_colors(n_categories)

    # 设置默认explode（如果没有提供）
    if explode is None:
        explode = [0.03] * n_categories  # 轻微分离所有扇形

    # 创建饼图
    fig, ax = plt.subplots(figsize=(max(8, n_categories * 1.5), 6))  # 根据类别数调整宽度
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=autopct,
        startangle=90,
        explode=explode,
        colors=colors,
        wedgeprops={"linewidth": 0.8, "edgecolor": "white"},
        textprops={"fontsize": 10, "color": "#333333"},
        pctdistance=0.8,  # 百分比文字位置
    )

    # 设置标题
    plt.title("行业分布饼图", fontsize=14, pad=20, color="#555555")

    # 调整标签位置防止重叠
    plt.tight_layout()

    # 添加图例（当类别过多时）
    if n_categories > 5:
        plt.legend(wedges, labels, title="分类", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)

    # 保存图片
    plt.savefig(filename, dpi=720, bbox_inches="tight", transparent=True)
    plt.close()
    return filename


# 使用示例（测试不同数据量）
# for n in [3, 5, 8, 12]:
#     data = {f"类别{i+1}": np.random.randint(1, 10) for i in range(n)}
#     print(data)
#     draw_pie_chart(data=data, title=f"{n}个分类的示例饼图", filename=f"pie_chart_{n}_categories.png")
