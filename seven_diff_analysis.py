from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import pandas as pd
import seaborn as sns


class SevenDiffAnalysis(Template_Task_Statistics):
    path = '../data_ocd_metacognition/tasks_data/seven_diff'
    csv_block_shocking = pd.read_csv('../statistical_analysis_tasks/other/csv_block_shocking.csv')

    def get_no_trials(self, block='all'):
        """
        :param block: The block of image you are interested in, between all, shocking, non-shocking, calligraphy and
        chess
        :return: numbers of corresponding trials
        """
        if block == 'all':
            numbers_trials = np.arange(0, 200)
        elif block == 'shocking' or block == 'non-shocking':
            numbers_trials = self.csv_block_shocking[self.csv_block_shocking['block'] == block]['no_trial']
        elif block == 'calligraphy':
            numbers_trials = np.arange(100, 150)
        elif block == 'chess':
            numbers_trials = np.arange(150, 200)
        return numbers_trials

    def success_rate_trials(self, df):
        diff = abs(df['ans_candidate'] - df['good_ans'])
        condlist = [diff == 0, diff == 1, diff == 4, diff == 5, diff == 6]
        # choicelist = [1, 2 / 3, 2 / 3, 1 / 3, 0] SI ON VEUT PONDERER
        choicelist = [1, 0, 0, 0, 0]
        resultat = np.select(condlist, choicelist)

        success = [np.mean(resultat[:n]) * 100 for n in range(1, len(resultat) + 1)]
        return np.array(success)

    def stats(self, block='all', save_tab=True):
        """
        :param block : The block you are interested in, change regarding tasks (default = 'all')
        :param save_tab : whether you want to save the output in a csv file
        :return: dataframe containing descriptive statistics of the data for every subjects
        """
        tab1 = self.base_stats(block=block)
        numbers_trials = self.get_no_trials(block)
        average_diff = []
        choicelist = [0, 1, 2, 3]
        for df in self.df_files:
            if block != 'all':
                df = df[df['no_trial'].isin(numbers_trials)]
                if len(df) == 0:
                    continue
            ans = df['ans_candidate']
            condlist = [ans == 0, ans == 1, ans == 5, ans == 6]
            res = np.select(condlist, choicelist)
            average_diff.append(np.mean(res))  # something weird here
        tab1['Average Difference'] = average_diff
        print(tab1)
        if save_tab:
            tab1.to_csv(f'../statistical_analysis_tasks/stats_jpg/seven_diff/stats_seven_diff_{block}.csv', index=False)
        return tab1

    def plot_pourcentage(self, disorder='ocd', block="all", border=False, save_fig=True):
        """ Create a graph representing success rate depending on the number of trials
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param block: the block of images you are interested in between all, shocking, non-shocking, calligraphy and chess
        :param border: True, if you want margins of the result for each group, False otherwise (default = False)
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
        """
        plt.figure()
        plt.suptitle(f'Success rate function of the number of the trial for Seven Differences Task')
        plt.title(f"(block = {block})", fontsize=10)
        self.all_success_plot(disorder='ocd', block=block, border=border, max_len=200)
        plt.legend(self.custom_lines,
                   [f"Healthy Control (n={self.total_people('none')})",
                    f'{self.list_graph_name[self.list_disorder.index(disorder)]} (n={self.total_people(disorder)})'])
        plt.ylabel('Success rate (%)')
        plt.xlabel("N trials")
        plt.grid(False)
        plt.ylim(0, 100)
        plt.tight_layout()
        if save_fig:
            plt.savefig(f'../statistical_analysis_tasks/stats_jpg/seven_diff/Success_rate_trials(Block = {block}).jpg')
        plt.show()

    def boxplot_average(self, category='Success rate', disorder='ocd', block='all', save_fig=True):
        """Create boxplot of the average result from a specific category for HC group and considered disorder group
        :param category: the category of the output of stats that you want to see
        :param disorder: the disorder you are interested in (default = 'ocd')
        :param block: the block of images you are interested in between all, shocking, non-shocking, calligraphy and chess
        :param save_fig: True, if you want to save the graphic as a picture, False otherwise (default = False)
            """
        if block != 'all':
            stats = self.stats(block=block)
        else:
            stats = self.stats()
        if disorder == 'all':
            tab = [stats[stats['disorder'] == 0][category], stats[stats['disorder'] != 0][
                category]]
        else:
            tab = [stats[stats['disorder'] == 0][category],
                   stats[stats['disorder'] == self.list_disorder.index(disorder)][
                       category]]
        success = pd.DataFrame({"Healthy Control": tab[0],
                                f'{self.list_graph_name[self.list_disorder.index(disorder)]}': tab[1]
                                })

        my_pal = {"Healthy Control": self.col[0],
                  f'{self.list_graph_name[self.list_disorder.index(disorder)]}': self.col[1]}
        plt.figure()
        plt.suptitle(f'{category} for Seven Differences Task')
        plt.title(f'(Block = {block})', fontsize=10)
        sns.boxplot(data=success, palette=my_pal)
        if category == 'Success rate':
            plt.ylabel(f'{category} (%)')
        else:
            plt.ylabel(f'{category}')
        if save_fig:
            plt.savefig(
                f'../statistical_analysis_tasks/stats_jpg/seven_diff/Boxplot:{category} Task (Block = {block}).png')
        plt.show()

    def average_diff(self):
        df = self.df_files[0]
        good_ans = df['good_ans']
        condlist = [good_ans == 0, good_ans == 1, good_ans == 5, good_ans == 6]
        choicelist = [0, 1, 2, 3]
        df['good_ans'] = np.select(condlist, choicelist)  # replace 5 and 6 values by 3 and 4
        return np.mean(df['good_ans'])

    def plot_reaction_time(self, block='all', disorder='ocd', border=False, max_len=200):
        list_patients = self.get_list_patients(disorder)
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            if block != 'all':
                numbers_trials = self.get_no_trials(block)
                df = df[df['no_trial'].isin(numbers_trials)]
            id = self.get_id(df)
            i = int(list_patients[list_patients[0] == id][1])
            if i != -1:
                tab = df['reaction_time']
                if len(tab) != max_len:
                    size = len(tab)
                    tab = np.resize(tab, max_len)
                    tab_empty_val = np.empty(tab[size:max_len].shape)
                    tab_empty_val = tab_empty_val.fill(np.nan)
                    tab[size:max_len] = tab_empty_val
                if i == 0:
                    HC_group.append(tab)
                else:
                    disorder_group.append(tab)
        if border:
            list_group = [HC_group, disorder_group]
            for i in range(2):
                plt.plot(np.nanmin(list_group[i], axis=0), self.col[i], alpha=0.25)
                plt.plot(np.nanmax(list_group[i], axis=0), self.col[i], alpha=0.25)
                plt.fill_between(np.arange(0, max_len), np.nanmin(list_group[i], axis=0),
                                 np.nanmax(list_group[i], axis=0),
                                 color=self.col[i], alpha=0.25)
        sns.lineplot(data=np.nanmean(HC_group, axis=0), color=self.col[0])
        sns.lineplot(data=np.nanmean(disorder_group, axis=0), color=self.col[1])
        plt.show()

    def tests_seven_diff(self):
        stats_seven_diff_all = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_all.csv')
        stats_seven_diff_shocking = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_shocking.csv')
        stats_seven_diff_nonshocking = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_non-shocking.csv')
        stats_seven_diff_calligraphy = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_calligraphy.csv')
        stats_seven_diff_chess = pd.read_csv('stats_jpg/seven_diff/stats_seven_diff_chess.csv')

        print("All \n --------------------\n")
        print(np.mean(stats_seven_diff_all[stats_seven_diff_all["disorder"] == 0]["Success rate"]))
        print(np.mean(stats_seven_diff_all[stats_seven_diff_all["disorder"] == 0]["Average reaction time"]))
        print(np.mean(stats_seven_diff_all[stats_seven_diff_all["disorder"] == 1]["Success rate"]))
        print(np.mean(stats_seven_diff_all[stats_seven_diff_all["disorder"] == 1]["Average reaction time"]))
        print(stats.ttest_ind(stats_seven_diff_all[stats_seven_diff_all["disorder"] == 0]["Success rate"],
              stats_seven_diff_all[stats_seven_diff_all["disorder"] == 1]["Success rate"]))
        print(stats.ttest_ind(stats_seven_diff_all[stats_seven_diff_all["disorder"] == 0]["Average reaction time"],
              stats_seven_diff_all[stats_seven_diff_all["disorder"] == 1]["Average reaction time"]))

        print("Shocking \n --------------------\n")
        print(np.mean(stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 0]["Success rate"]))
        print(np.mean(stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 0]["Average reaction time"]))
        print(np.mean(stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 1]["Success rate"]))
        print(np.mean(stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 1]["Average reaction time"]))
        print(stats.ttest_ind(stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 0]["Success rate"],
              stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 1]["Success rate"]))
        print(stats.ttest_ind(stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 0]["Average reaction time"],
              stats_seven_diff_shocking[stats_seven_diff_shocking["disorder"] == 1]["Average reaction time"]))


        print("Non-shocking \n --------------------\n")
        print(np.mean(stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 0]["Success rate"]))
        print(np.mean(stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 0]["Average reaction time"]))
        print(np.mean(stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 1]["Success rate"]))
        print(np.mean(stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 1]["Average reaction time"]))
        print(stats.ttest_ind(stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 0]["Success rate"],
                              stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 1]["Success rate"]))
        print(stats.ttest_ind(stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 0]["Average reaction time"],
                              stats_seven_diff_nonshocking[stats_seven_diff_nonshocking["disorder"] == 1]["Average reaction time"]))

        print("Calligraphy \n --------------------\n")
        print(np.mean(stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 0]["Success rate"]))
        print(np.mean(stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 0]["Average reaction time"]))
        print(np.mean(stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 1]["Success rate"]))
        print(np.mean(stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 1]["Average reaction time"]))
        print(stats.ttest_ind(stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 0]["Success rate"],
                              stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 1]["Success rate"]))
        print(stats.ttest_ind(stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 0]["Average reaction time"],
                              stats_seven_diff_calligraphy[stats_seven_diff_calligraphy["disorder"] == 1]["Average reaction time"]))

        print("Chess \n --------------------\n")
        print(np.mean(stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 0]["Success rate"]))
        print(np.mean(stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 0]["Average reaction time"]))
        print(np.mean(stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 1]["Success rate"]))
        print(np.mean(stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 1]["Average reaction time"]))
        print(stats.ttest_ind(stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 0]["Success rate"],
                            stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 1]["Success rate"]))
        print(stats.ttest_ind(stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 0]["Average reaction time"],
                            stats_seven_diff_chess[stats_seven_diff_chess["disorder"] == 1]["Average reaction time"]))
