import matplotlib.pyplot as plt

def plot_category_chart(stats_df, save_path='ai_category_chart.png'):
    """接收统计好的DataFrame，画柱状图并保存"""
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=[8, 5])
    plt.bar(stats_df['AI分类'], stats_df['数量'], color='skyblue', edgecolor='black')
    plt.title('AI 图书分类数量统计', fontsize=12)
    plt.xlabel('图书分类', fontsize=12)
    plt.xticks(rotation=45)
    plt.ylabel('数量', fontsize=12)

    for i, v in enumerate(stats_df['数量']):
        plt.text(i, v + 0.05, str(v), ha='center', va='bottom', fontsize=12)
    plt.savefig(save_path, bbox_inches='tight')
    plt.show()
    print(f'图表已保存至: {save_path}')
