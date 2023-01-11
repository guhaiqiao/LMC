from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd


languages = ['python', 'java', 'js']
language_name = {
    'python': 'Python',
    'java': 'Java',
    'js': 'JavaScript'
}
markers = {
    'python': 's',
    'java': '^',
    'js': 'o'
}
colors = {
    'python': '#1f77b4',
    'java': '#ff7f0e',
    'js': '#2ca02c'
}
# num of active projects 2005-2020
project_total_nums = {
    'python': np.array([395, 624, 978, 1712, 2986, 4990, 8508, 14239, 20858, 27524, 35908, 36884, 38486, 41270, 48780, 53566]),
    'java': np.array([446, 692, 1008, 1521, 2253, 3611, 6221, 9956, 14605, 20198, 27490, 27656, 25074, 22230, 21840, 21005]),
    'js': np.array([45, 104, 226, 526, 1309, 3509, 8666, 18294, 31036, 44656, 60568, 60066, 55971, 51858, 50928, 51802]),
}
count = 0


def draw_migration_evo(years, datas, save_path, ylabel, prop=False):
    fig, ax = plt.subplots(figsize=(4, 2.5))
    for language in languages:
        for data in datas:
            global count
            if count % 2 == 0:
                ls = ':'
                name = language_name[language] + ' Ungrouped'
            else:
                ls = '-'
                name = language_name[language] + ' Grouped'
            count += 1
            if prop:
                ax.plot(years, data[language] / project_total_nums[language],
                        color=colors[language], ls=ls, label=name, marker=markers[language], markersize=4)
            else:
                ax.plot(years, data[language], color=colors[language],
                        ls=ls, label=name, marker=markers[language], markersize=4)
    ax.set_xlabel("Year")
    ax.set_xticks(np.arange(2005, 2021, 3))
    ax.set_ylabel(ylabel)
    ax.legend(title='', loc='upper left', fontsize=7)
    plt.savefig(f"pic/{save_path}.pdf", bbox_inches="tight", dpi=200)
    plt.show()










