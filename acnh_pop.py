from selenium import webdriver 
from selenium.webdriver.common.by import By      
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import kaggle
import os
import zipfile
import glob
import time
from datetime import datetime as dt
from shutil import copyfile, rmtree

class AC_Popularity:

    def __init__(self, *args, **kwargs):
        self_path = os.path.dirname(os.path.realpath(__file__))

    def create_df(self, *args, **kwargs):
        # Create a DataFrame
        self_path = os.path.dirname(os.path.realpath(__file__))
        path = self_path
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver', options=options)
        driver = webdriver.Chrome(options=options)


        url =  'https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php'
        driver.get(url)
        classes = driver.find_elements(By.CLASS_NAME, "c-candidate-name")
        for x in range(len(classes)):
            if classes[x].is_displayed():
                driver.execute_script("arguments[0].click();", classes[x])
                time.sleep(5)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'lxml')

        tier_data = soup.find_all(class_="c-tier")
        tier_list = list(tier_data)

        villager_tier = []
        villager_name = []
        villager_rank = []
        villager_value = []

        for i in tier_list:
            index = tier_list.index(i)
            tier = list(tier_list[index].find(class_="u-grow flex").find('p'))
            value = list(tier_list[index].find(class_="c-badge u-hiddenMobile"))
            villager_data = list(tier_list[index].find_all(class_="cc-candidate-container flex"))

            for i in villager_data:
                soup = villager_data[villager_data.index(i)]

                villager_tier.append(tier[0])
                villager_value.append(value[0])
                villager_name.append(soup.find(class_="c-candidate-name").get_text())
                villager_rank.append(soup.find(class_="c-candidate-rank").get_text())

                # Reset Soup at End
                if villager_data[-1] == i:
                    soup = BeautifulSoup(page_source, 'lxml')

        villager_field_dict = {
        'villager_name': villager_name,
        'villager_tier_rank': villager_rank,
        'villager_tier': villager_tier,
        'villager_value': villager_value}

        # Create df
        self.df = pd.DataFrame(villager_field_dict)
        df = self.df

        # Clean Up
        tier_dict = {'TIER 1': 1, 
                    'TIER 2': 2, 
                    'TIER 3': 3, 
                    'TIER 4': 4, 
                    'TIER 5': 5, 
                    'TIER 6': 6}

        df['villager_tier_num'] = df['villager_tier'].apply(lambda x: tier_dict[x])
        df.sort_values(by=['villager_tier_num', 'villager_tier_rank'])
        df['villager_rank'] = df.index+1
        df['Date_Pulled'] = datetime.date.today()

        # Name Changes for Join
        def name_change(x):
            
            name_dict = {
            'Renee': 'Renée',
            'OHare': "O'Hare",
            'Buck(Brows)': 'Buck',
            'WartJr': 'Wart Jr.',
            'Crackle(Spork)': 'Spork'}

        
            if x in list(name_dict.keys()):
                name = name_dict[x]
            else:
                name = x
            return name

        df['villager_name'] = df['villager_name'].apply(lambda x: name_change(x))
        
    def kaggle_data(self, *args, **kwargs):
        
        path = os.path.dirname(os.path.realpath(__file__))

        # Check Directory for villagers.csv
        acdir = glob.glob(path + '/*')
        
        file_check = any('villagers.csv' in file for file in acdir)

        if file_check == False:
            # Kaggle Setup
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files('jessicali9530/animal-crossing-new-horizons-nookplaza-dataset', path = path)

            # Unzip Download
            path_before = path + '/animal-crossing-new-horizons-nookplaza-dataset.zip'
            path_after = path + '/animal-crossing-new-horizons-nookplaza-dataset'

        
            with zipfile.ZipFile(path_before, 'r') as zip_ref:
                zip_ref.extractall(path_after)
        
            # Copy Villager File to Root
            copyfile(path_after + '/villagers.csv', path + '/villagers.csv')# Move villagers.csv to project directory
            
            # Remove Other Downloaded Files
            os.remove(path_before)
            rmtree(path_after)
        
    def join_tables(self, *args, **kwargs):

            path = os.path.dirname(os.path.realpath(__file__))
            
            # Import Dataframes to Python and Merge
            self.df_kag = pd.read_csv(path + '/villagers.csv')
            self.df_final = pd.merge(self.df, self.df_kag, how='left', left_on=['villager_name'], right_on=['Name'])
            df_final = self.df_final
            
            # Clean Birthday field
         
            def birthday_clean(x):
                x = str(x)
                try:
                    bdate = dt.strptime(x, '%d-%b')
                    bdate = bdate.replace(year = 2020)
                    bdate = bdate.date()
                except:
                    bdate = 'N/A'
                
                return bdate
         
            df_final['Birthday'] = df_final['Birthday'].apply(lambda x: birthday_clean(x))
         
            # Clean Column Names - No Spaces
         
            for column in list(df_final.columns):
                old = column
                new = column.replace(' ', '_')
                
                if old == new:
                    continue
                else:
                   df_final.rename(columns={old:new}, inplace=True)

    def send_csv(self, *args, **kwargs):
        csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'acnh_villagers.csv')
        self.df_final.to_csv(csv_path, index=False)


#Procedure
        
print(f'✅ Villager data collection started at {datetime.datetime.now()}')
ac = AC_Popularity()
ac.create_df()
ac.kaggle_data()
ac.join_tables()
ac.send_csv()

print(f'✅ Villager data collection finished at {datetime.datetime.now()}')