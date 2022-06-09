from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class seven_diff_analysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/seven_diff'

    def get_no_trials(self, type_image='all'):
        if type_image == 'all':
            numbers_trials = np.arange(0, 201)
        elif type_image == 'shocking':
            numbers_trials = np.arange(0, 50)
        elif type_image == 'non-shocking':
            numbers_trials = np.arange(51, 101)
        elif type_image == 'calligraphy':
            numbers_trials = np.arange(101, 151)
        elif type_image == 'chess':
            numbers_trials = np.arange(151, 201)
        return numbers_trials

    def success_rate_trials_penalized(self, df):
        diff = abs(df['ans_candidate'] - df['good_ans'])
        condlist = [diff == 0, diff == 1, diff == 4, diff == 5, diff == 6]
        choicelist = [1, 2 / 3, 2 / 3, 1 / 3, 0]
        resultat = np.select(condlist, choicelist)
        success = [np.mean(resultat[:n]) * 100 for n in range(1, len(resultat) + 1)]
        return np.array(success)

    def plot_pourcentage(self, mental_disorder=True, disorder='ocd', type_image="all", border=False):
        """
        :param mental_disorder: put False if you want all data without any distinction otherwise put True
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param type_image: the type or image you are interested between all, shocking, non-shocking, calligraphy and chess
        """
        custom_lines = [plt.Line2D([0], [0], color=self.col[0], lw=4), plt.Line2D([0], [0], color=self.col[1], lw=4)]
        list_patients = self.get_list_patients(disorder)

        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Seven Differences Task ')
        plt.title(f'(Block = {type_image})', fontsize=10)

        numbers_trials = self.get_no_trials(type_image)
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            df = df[df['no_trial'].isin(numbers_trials)]
            if i != -1:
                tab = self.success_rate_trials_penalized(df)
                if len(tab) != 200:
                    size = len(tab)
                    tab = np.resize(tab, (200))
                    tab_empty_val = np.empty(tab[size:200].shape)
                    tab_empty_val = tab_empty_val.fill(np.nan)
                    tab[size:200] = tab_empty_val
                if i == 0:
                    HC_group.append(tab)
                else:
                    disorder_group.append(tab)

        mean_HC_group = np.nanmean(HC_group, axis=0)

        mean_dis_group = np.nanmean(disorder_group, axis=0)
        if mental_disorder:
            plt.legend(custom_lines, [f'Healthy Control', f'{self.list_graph_name[self.list_disorder.index(disorder)]}'])
        sns.lineplot(data=mean_HC_group, color=self.col[0])

        sns.lineplot(data=mean_dis_group, color=self.col[1])
        if border == True:
            min_HC_group = np.nanmin(HC_group, axis=0)
            max_HC_group = np.nanmax(HC_group, axis=0)
            min_disorder = np.nanmin(disorder_group, axis=0)
            max_disorder = np.nanmax(disorder_group, axis=0)
            plt.plot(max_disorder, color=self.sub_col[1], alpha=0.5)
            plt.plot(min_disorder, color=self.sub_col[1], alpha=0.5)
            plt.plot(min_HC_group, color=self.sub_col[0], alpha=0.5)
            plt.plot(max_HC_group, color=self.sub_col[0], alpha=0.5)
            plt.fill_between(np.arange(0, 200), min_HC_group, max_HC_group, color=self.sub_col[0], alpha=0.5)
            plt.fill_between(np.arange(0, 200), min_disorder, max_disorder, color=self.sub_col[1], alpha=0.5)
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(True)
        plt.tight_layout()
        plt.show()


def boxplot_average(self, category='success_rate', disorder='ocd', type_image="all"):
    """
        :param disorder:
        :param category:
        :param type_image: the type or image you are interested between all, various, calligraphy and chess
        """
    if type_image != 'all':
        stats = self.stats(specific_type=True, type=type_image)
    else:
        stats = self.stats()
    if disorder == 'all':
        success = pd.DataFrame({"Healthy Control": stats[stats['disorder'] == 0][category],
                                disorder: stats[stats['disorder'] != 0][
                                    category]})
        mean_success = success.apply(np.mean, axis=0)
    else:
        success = pd.DataFrame({"Healthy Control": stats[stats['disorder'] == 0][category],
                                disorder: stats[stats['disorder'] == self.list_disorder.index(disorder)][
                                    category]})
        mean_success = [np.mean(stats[stats['disorder'] == 0][category]),
                        np.mean(stats[stats['disorder'] == self.list_disorder.index(disorder)][category])]

    plt.figure()
    success[["Healthy Control", disorder]].plot(kind='box', title=f'Boxplot of {category} '
                                                                  f'for the task seven diff (part = {type_image})')
    plt.ylabel(f'{category}')
    plt.tight_layout()
    plt.show()

    plt.figure()
    plt.title(f'Comparaison of {category} for the task seven diff (block = {type_image})')
    plt.bar(range(len(mean_success)), mean_success, color=self.col)
    plt.xticks(range(len(mean_success)), ["Healthy Control", disorder])
    plt.ylabel(f'{category}')
    plt.tight_layout()
    plt.show()


s = seven_diff_analysis()
s.plot_pourcentage()
