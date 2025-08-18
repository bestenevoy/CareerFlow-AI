import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from wordcloud import WordCloud
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
    # 筛选前20个较大值
    if len(parsed_data) > 15:
        parsed_data = {k: v for k, v in sorted(parsed_data.items(), key=lambda item: len(item[1]), reverse=True)[:15]}
    industries = list(parsed_data.keys())
    salaries = [parsed_data[industry] for industry in industries]

    # 绘制箱型图
    plt.figure(figsize=(16, 9))
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

    # 根据用户的要求，将筛选出的前20个较大值保存为字典
    # 筛选前20个较大值
    if len(data) > 15:
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)[:15]}

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
        explode = [0.05] * n_categories  # 轻微分离所有扇形

    # 创建饼图
    fig, ax = plt.subplots(figsize=(16, 8))  # 根据类别数调整宽度
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=autopct,
        startangle=90,
        explode=explode,
        colors=colors,
        wedgeprops={"linewidth": 0.8, "edgecolor": "white"},
        textprops={"fontsize": 10, "color": "#333333"},
        pctdistance=0.5,  # 百分比文字位置
    )

    # 设置标题
    plt.title("行业分布饼图", fontsize=14, pad=20, color="#555555")

    # 调整标签位置防止重叠
    plt.tight_layout()

    # 添加图例（当类别过多时）
    if n_categories > 5:
        plt.legend(wedges, labels, title="分类", loc="center left", bbox_to_anchor=(1.1, 0.5), fontsize=9)

    # 保存图片
    plt.savefig(filename, dpi=720, bbox_inches="tight", transparent=True)
    return filename

def generate_low_saturation_wordcloud(data_dict, filename, title="词云", 
                                     figsize=(16, 9), background_color='white', font_path=None):
    """
    生成低饱和度美观词云
    
    参数:
    - data_dict: 包含词语和对应频次的字典
    - title: 图表标题
    - figsize: 图表大小
    - background_color: 背景颜色
    - font_path: 中文字体路径(Windows: 'C:/Windows/Fonts/simhei.ttf', 
                 Mac: '/System/Library/Fonts/PingFang.ttc')
    """
    
    # 设置中文字体（如果未提供字体路径，尝试自动检测）
    if font_path is None:
        # 尝试常见的中文字体路径
        possible_fonts = [
            'C:/Windows/Fonts/simhei.ttf',  # Windows
            '/System/Library/Fonts/PingFang.ttc',  # Mac
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Linux
            '/System/Library/Fonts/STHeiti Medium.ttc'  # Mac 另一种字体
        ]
        
        for font in possible_fonts:
            try:
                # 检查字体文件是否存在
                with open(font, 'rb'):
                    font_path = font
                    break
            except:
                continue
    
    # 创建词云对象
    wordcloud = WordCloud(
        background_color=background_color,
        width=figsize[0]*100,
        height=figsize[1]*100,
        font_path=font_path,  # 指定中文字体
        colormap='tab20',  # 使用低饱和度的蓝色调
        max_words=200,
        contour_width=1,
        contour_color='lightgray',
        relative_scaling=0.5
    )
    
    # 生成词云
    wordcloud.generate_from_frequencies(data_dict)
    
    # 显示词云
    plt.figure(figsize=figsize)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, pad=20)
    plt.tight_layout()
    plt.savefig(filename, dpi=720, bbox_inches="tight", transparent=True)
    return filename

if __name__ == "__main__":
    # 示例数据字典
    word_freq = {
        '产品A': 100,
        '产品B': 80,
        '产品C': 60,
        '产品D': 40,
        '产品E': 20,
        '产品F': 10,
        '产品G': 15,
        '产品H': 25,
        '产品I': 35,
        '产品J': 45,
        '产品K': 55,
        '产品L': 65,
        '产品M': 75,
        '产品N': 85,
        '产品O': 95
    }

    # 调用函数生成词云
    generate_low_saturation_wordcloud(word_freq, "a.jpg", title="2023年产品词云")




# 使用示例（测试不同数据量）
# for n in [3, 5, 8, 12]:
#     data = {f"类别{i+1}": np.random.randint(1, 10) for i in range(n)}
#     print(data)
#     draw_pie_chart(data=data, title=f"{n}个分类的示例饼图", filename=f"pie_chart_{n}_categories.png")
