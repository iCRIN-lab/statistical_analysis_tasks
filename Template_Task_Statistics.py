import numpy as np
import pandas as pd
import glob
import os
import scipy.stats as sps
import seaborn as sns
import matplotlib.pyplot as plt


class Template_Task_Statistics:
    """ The redcap export in csv, change the path every time with the correct one"""
    redcap_csv = pd.read_csv("STOCADPinelfollowup_DATA_2022-12-05_1143.csv", sep=',')

    """ List of diminutives of the disorder with index corresponding to the number in the redcap, 
    names can be change except 'all' but the order cannot be changed """
    list_disorder = ['all', 'ocd', 'du', 'db', 'ta', 'tus', 's']

    """ List of corresponding names to be shown in graphics"""
    list_graph_name = ['All disorders', 'OCD', 'Unipolar Depression', 'Bipolar Depression', 'Anxiety Disorder',
                       'Substance Use Disorder', 'Schizophrenia']

    """ Color for the graph, respectfully the color for healthy control representation and the color for the considered 
    disorder representation"""
    col = ['royalblue', 'crimson']

    """ Specific lines to get the color and the category to always match in the legend"""
    custom_lines = [plt.Line2D([0], [0], color=col[0], lw=4), plt.Line2D([0], [0], color=col[1], lw=4)]

    """ Path of the file, which is set in every class analysis"""
    path = ""
    """list des patients, 0 = HC ; 1 = TOC ; 2 = Other diseases"""
    list_patients = [1, 1, 0, 0, 0, 0, 1, 1, 0, 2, 1, 2, 0, 0, 2, 1, 0, 2, 0, 0, 1, 0, 2, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                     0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 0, 0, 2, 0, 0, 0,
                     0, 0, 0]

    def __init__(self, pratice=False):
        """
        :param pratice: if you want to keep to the practice in the analysis put pratice=True
        """

        self.csv_files = glob.glob(os.path.join(self.path, "*.csv"))
        self.csv_files.sort(key=lambda x: x.split("_")[5])
        self.df_files = [pd.read_csv(f, encoding='ISO-8859-1') for f in self.csv_files]

        """ Deleting all the lines corresponding to the pratice from all the csv
        """
        for j in range(len(self.df_files)):
            if not pratice:
                i = 0
                while self.df_files[j].no_trial[i] != 0:
                    i += 1
                self.df_files[j] = self.df_files[j].drop(np.arange(i))

    def get_id(self, df):
        """ Get the redcap id from a specific dataframe
        :param df : resulting dataframe from a task
        :return : number of their id
        """
        return int(str(df['id_candidate'].tail(1).item())[8:11])

    def get_list_patients(self, disorder="ocd"):
        """" Get the list of people with the considered disorder
        :return a dataframe with the id of the subject and 1 or 0 if the subject has the considered disorder
        """
        all_disorder = np.array(self.redcap_csv['diagnostic_principal'])
        if disorder == 'all':
            list_patients = np.where(all_disorder == 0, 0, 1)
        else:
            list_patients = np.select([all_disorder == 0, all_disorder == self.list_disorder.index(disorder)],
                                      [0, 1], -1)
        return pd.DataFrame(np.array([np.array(self.redcap_csv.record_id), list_patients]).T)

    def get_eeg_patient(self):
        return [raw[0] for raw in self.redcap_csv.values if (raw[32] == 1 or raw[34] == 1)]


    def success_rate_trials(self, df):
        """ Get the success_rate regarding trials from the column result of the dataframe
        :param df: resulting dataframe from a task
        :return: an array with the success rate regarding no_trial for considered dataframe
        """
        success = [np.mean(df["result"][:n]) * 100 for n in range(1, len(df['result']) + 1)]
        return np.array(success)

    def base_stats(self, block='all'):
        """ Standard statistical result for all tasks
        :param block : The block you are interested in, change regarding tasks (default = 'all')
        :return: dataframe containing descriptive statistics of the data for every subjects
        """
        numbers_trials = self.get_no_trials(block)
        tab = []
        for df in self.df_files:
            if block != 'all':
                df = df[df['no_trial'].isin(numbers_trials)]
                if len(df) == 0:
                    continue
            id = self.get_id(df)
            disorder_id = self.redcap_csv[self.redcap_csv.record_id == id]['diagnostic_principal']
            tab.append([id, disorder_id.iloc[0], round(np.mean(df['result']) * 100, 2), round(float(np.mean(df['reaction_time'])), 2),
                        np.max(df['reaction_time'])])
        tab = pd.DataFrame(tab)
        tab.columns = ['Id', 'disorder', 'Success rate', 'Average reaction time', 'Maximum reaction time']
        return tab

    def stats(self):
        """
        :param block : The block you are interested in, change regarding tasks (default = 'all')
        :return: dataframe containing descriptive statistics of the data for every subjects
        """

    def total_people(self, disorder='ocd'):
        """ Get the number of person in the healthy control group and the considered disorder group in our data (using
        stats, so you can have the number for a specific task without taking in consideration empty csv)
        :param disorder: the specific disorder you which to look at between the list_disorder, if you want healthey control group put 'none' (default= 'ocd')
        :return: size of disorder group
        """
        stats = self.stats()
        if disorder == 'none':
            return len(stats[stats.disorder == 0])
        elif disorder == 'all':
            return len(stats[stats.disorder != 0])
        else:
            return len(stats[stats.disorder == self.list_disorder.index(disorder)])

    def get_no_trials(self, *args):
        """ Get the numbers of trials within a certain category
        """

    def all_success_plot(self, border=False, block='all', disorder='ocd', max_len=200):
        """ Baseline to plot the success rate regarding trials without title and legends
        :param border: True, if you want margins of the result for each group (default = False)
        :param block: The specific block or block of lucifer you are interested in (default = 'all')
        :param disorder: The specific disorder you are interested in (default = 'ocd')
        :param max_len: The maximum size of trial for the considered task
        """
        list_patients = self.get_list_patients(disorder)
        HC_group = []
        disorder_group = []
        for df in self.df_files:
            id = self.get_id(df)
            i = list_patients[list_patients[0] == id][1].iloc[0]
            if block != 'all':
                numbers_trials = self.get_no_trials(block)
                df = df[df['no_trial'].isin(numbers_trials)]
                if len(df) == 0:
                    continue
            if i != -1:
                tab = self.success_rate_trials(df)
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
        return np.nanmean(HC_group, axis=0), np.nanmean(disorder_group, axis=0)

    def plot_pourcentage(self, *args):
        """ Create a graph representing success rate depending on the number of trials
            """
    def test_success_rate(self, *args):
        """
        Perform t-tests on results tab for each task
        """


    def boxplot_average(self, *args):
        """ Create boxplot of the average result from a specific category for HC group and considered disorder group
        """

    def group_comparison(self, block='all', category='Success rate', disorder='ocd', print_status=True):
        """" Student test for considered criteria
        :param print_status:
        :param block: The specific block or block of lucifer you are interested in (default = 'all')
        :param category: the category of the output of stats that you want to see between
        'Success rate', 'Average reaction time', 'Maximum reaction time' for all task and 'Average count image',
        'Maximum count image', 'Minimum count image', 'Success/count image' for where is tockie (default = 'Success rate')
        :param disorder: The disorder you want to compare with control group (default = 'ocd')
        """
        X = self.stats(block=block)
        X1 = np.array(X[X.disorder == 0][category])
        X2 = np.array(X[X.disorder == self.list_disorder.index(disorder)][category])
        if print_status:
            if block != 'all':
                print(
                    f'Pour le test de student sur la catégorie {category} entre les sujets sains et les sujets {disorder}'
                    f' pour le block {block} , on obtient une p-value de ', sps.ttest_ind(X1, X2)[1])
            else:
                print(
                    f'Pour le test de student sur la catégorie {category} entre les sujets sains et les sujets {disorder}'
                    f' , on obtient une p-value de ', sps.ttest_ind(X1, X2)[1])

            if sps.ttest_ind(X1, X2)[1] > 0.05:
                print("Il n'y a pas de différence significative entre les deux groupes comparés")
            else:
                print("Il y a une différence significative entre les deux groupes comparés")
        return sps.ttest_ind(X1, X2)[1]

    def get_disorder_stats(self, block='all', disorder='ocd', save_tab=False):
        """ Get the dataframe stats for a specific disorder
        :param disorder: The specific disorder you are interested in (default = 'ocd'),
        if you want HC control group put 'none'
        """
        if disorder == 'all':
            tab = self.stats(block=block)[self.stats(block=block).disorder != 0]
        elif disorder == 'none':
            tab = self.stats(block=block)[self.stats(block=block).disorder == 0]
        else:
            tab = self.stats(block=block)[self.stats(block=block).disorder == self.list_disorder.index(disorder)]
        if save_tab:
            if len(tab.columns) == 5:
                path = f'../statistical_analysis_tasks/stats_jpg/symmetry/stats_symmetry_{disorder}.csv'
            elif len(tab.columns) > 7:
                path = f'../statistical_analysis_tasks/stats_jpg/where_is_tockie/stats_wit_{disorder}.csv'
            elif len(tab.columns) == 6:
                if tab.columns[5] == 'group':
                    path = f'../statistical_analysis_tasks/stats_jpg/lucifer/stats_lucifer_{disorder}_{block}.csv'
                if tab.columns[5] == 'Average Difference':
                    path = f'../statistical_analysis_tasks/stats_jpg/seven_diff/stats_seven_diff_{disorder}_{block}.csv'

            tab.to_csv(path, index=False)
        return tab
