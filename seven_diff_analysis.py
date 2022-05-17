from Template_Task_Statistics import Template_Task_Statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class seven_diff(Template_Task_Statistics):

    def plot_pourcentage(self, mental_disorder=True, disorder='all', type_image="all"):
        """
        """
        col = ['black', 'red']
        if type_image == 'all':
            lim=np.array([-1, 202])
        if type_image == 'various':
            lim = np.array([0, 100])
        if type_image == 'calligraphy':
            lim = np.array([101, 150])
        if type_image == 'chess':
            lim = np.array([151, 200])

        plt.figure()
        plt.title(f'Success rate for the task seven diff regarding trials (part = {type_image})')
        for (df, i) in zip(self.df_files, self.get_list_patients(disorder)):
            if i != 1:
                tab = self.success_rate_trials(df)
                if mental_disorder:
                    plt.plot(tab, color=col[i])
                else:
                    plt.plot(tab, color='k')
            if mental_disorder:
                plt.legend(['no-disorder', disorder])
        plt.xlim(lim[0], lim[1])
        plt.show()

    def stats(self):
        df = self.df_files
        tab = pd.DataFrame(np.array(
                [df['id_candidate'][3], np.mean(df['result']), np.mean(df['reaction_time']),
        np.max(df['reaction_time']), np.min(df['reaction_time'])])).T
        tab.columns = ['Id', 'Success_rate', 'Average_reaction_time', 'max_reaction_time', 'min_reaction_time']
        return tab

a = seven_diff('/Users/melissamarius/Documents/all_csv/seven_diff')
a.plot_pourcentage()