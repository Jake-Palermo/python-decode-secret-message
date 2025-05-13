
import requests
from bs4 import BeautifulSoup
import pandas as pd

def getTable(url):
    #Retrieves the table from the url and returns it as a pandas DataFrame.
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    table = tables[0]
    rows = table.find_all('tr')
    headers = [th.get_text(strip=True) for th in rows[0].find_all(['th', 'td'])]
    
    data = []
    for row in rows[1:]:
        cells = row.find_all(['th', 'td'])
        if len(cells) == len(headers):
            data.append([cell.get_text(strip=True) for cell in cells])

    df = pd.DataFrame(data, columns=headers)

    return df

def printCharacters(url):
    df = getTable(url)

    #clean column names
    df.columns = [str(col).strip().lower() for col in df.columns]
    df.rename (columns={
        'x-coordinate': 'x',
        'y-coordinate': 'y',
        'character': 'char'
    }, inplace=True)

    #had to add this to avoid an error where inputs weren't valid integers
    df['x'] = pd.to_numeric(df['x'], errors='coerce')
    df['y'] = pd.to_numeric(df['y'], errors='coerce')

    #gets grid dimensions
    max_x = df['x'].max()
    max_y = df['y'].max()

    #creates the grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    #fills the grid with characters
    for _, row in df.iterrows():
        x, y, char = row['x'], row['y'], row['char']
        grid[y][x] = char  
    
    #prints the grid
    print("\nCharacter Grid:")
    for row in grid:
        print(''.join(row))




