from utils.scrapper import Scrapper
 
def data_scrapping() -> list: 
  scrapper = Scrapper()
  repos_list = scrapper.run() 
  return repos_list

def main():  
  repos_list = data_scrapping() # this will be fed into Macaron
  print(repos_list)



if __name__ == "__main__":
  
  main()
  