from difflib import SequenceMatcher
  
def plagiarism_checker(string1: str, string2:str):
    score = SequenceMatcher(None, string1,
                         string2).ratio()
      
    result = int(score*100)
    return result
