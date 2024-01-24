import fitz #pymuPDF
import os
import pandas as pd

def parse_pdf(file_path):
    #fitz breaks down pdf file to list of page
    doc = fitz.open(file_path)
    text = ''
    for page_number in range(0,1) :
        page = doc[page_number]
        text += page.get_text()
    doc.close()
    return text

file_path = r'C:\Users\asus\Downloads\griotsgarage'
file_name = 'Iron%20and%20Fallout%20Remover%20SDS%2010-6-2016.pdf'
parsed_text = parse_pdf(os.path.join(file_path,file_name))
#make list of individual text line splitted with return char
split_text = parsed_text.split('\n')
#remove all ' ' within the list
strip_spaces_text = [value for value in split_text if value != ' ']

#locate string precedes document product name
try :
    target_index = strip_spaces_text.index('Safety Data Sheet ')
except ValueError:
    print('Value not found')

print(strip_spaces_text)
print(target_index)
product_name = strip_spaces_text[target_index+1]
print(product_name)

#locate Section 3
try :
    target_index = strip_spaces_text.index('SECTION 3: COMPOSITION/INFORMATION ON INGREDIENTS ')
except ValueError:
    print('Value not found')
#locate end of section 3    
try :
    target_lastindex = strip_spaces_text.index('This composition consists of a combination of ingredients. The ones potentially contributing to classified hazards ')
except ValueError:
    print('Value not found')
    
dataframe_head = ['Product Name','Component','CAS No.','EC No','% Wt']
data_minusname = strip_spaces_text[(target_index+5):(target_lastindex-1)]
reshaped_data_minus_name = [data_minusname[i:i+4] for i in range(0,len(data_minusname),4)]
reshaped_data = [[product_name]+ each_record for each_record in reshaped_data_minus_name]

df = pd.DataFrame(reshaped_data,columns=dataframe_head)
print(df)