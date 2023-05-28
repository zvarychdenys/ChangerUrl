import sys
import requests
from bs4 import BeautifulSoup

class ChangerUrls():

    def __init__(self, current_filename, updates_filename) -> None:
        

        self.current_filename = current_filename
        self.updates_filename = updates_filename

        with open(current_filename) as file:
            self.file_contents = file.read()

        with open(self.updates_filename) as file:
            self.change_contents = file.read()

        self.check_current_elements()
        self.check_updates()

        self.apply_changes()

        self.save_changes()

    def check_current_elements(self): 

        soup = BeautifulSoup(self.file_contents, 'html.parser')

        id_attributes = soup.find_all('g', id=True)

        id_values = [elem['id'] for elem in id_attributes if 'elem_' in elem['id']]

        self.dict_id_hrefs = {}

        for id_value in id_values:

            g_elements = soup.find('g', id=id_value)

            a_elements = g_elements.find('a')

            try:
                href_element = a_elements.get('href')
                self.dict_id_hrefs[id_value] = href_element
            except:
                pass

        return self.dict_id_hrefs


    def check_updates(self): 
        
        self.change_dict = {}

        for change_content in self.change_contents.split(','):
            change_key = 'elem_' + change_content.split(' ')[0]
            self.change_dict[change_key] = change_content.split(' ')[1]

        return self.change_dict
        
    def apply_changes(self) -> str:

        soup = BeautifulSoup(self.file_contents, 'html.parser')

        for change_key, change_link in self.change_dict.items():
            
            g_elements = soup.find('g', id=change_key)
            a_elements = g_elements.find('a')
            
            if a_elements: 
                href = a_elements.get('href')
                a_elements['href'] = change_link

        self.output_changes = str(soup)     
        return self.output_changes

    def save_changes(self):
        
        with open('output.html', 'w') as file:
            file.write(self.output_changes)

if __name__ == "__main__":
    
    args = sys.argv

    changer_urls = ChangerUrls(args[1], args[2])