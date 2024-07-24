from urllib.request import urlopen
from bs4 import BeautifulSoup
from printing_output_evaluation import _col_text


def get_page_as_soup(url:str) -> BeautifulSoup:
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return BeautifulSoup(html, 'html.parser')

def get_most_recent_week_url(meal_plan:str="flexitarisk") -> tuple[str,str]:
    if meal_plan == "flexitarisk":
        flexitarisk_url = 'https://sundpaabudget.dk/kategori/madplaner/flexitariske-madplaner/'
    flexitarisk_page = get_page_as_soup(flexitarisk_url)
    
    all_weeks = flexitarisk_page.find_all(["article"])
    week_a_element = all_weeks[0].find_all("a")
    week_title = week_a_element[0]["title"]
    
    print(
        _col_text(
            string="Title of latest week: ",
            fore_colour="magenta",
            back_colour="black",
        ),
        _col_text(
            string=f"{week_title}",
            fore_colour="black",
            back_colour="magenta",
        )
    )
    
    most_recent_week = all_weeks[0].find_all("a", href=True)
    most_recent_week_url = most_recent_week[0]["href"]
    return week_title, most_recent_week_url

def get_days_urls(most_recent_week_url:str) -> list:
    
    week_page = get_page_as_soup(most_recent_week_url)

    week_p_tag = week_page.find_all(["p"])
    list_days_urls = []
    for a_element in week_p_tag:
        if a_element.findChild("strong"):
            strong_element = a_element.findChild("strong").string
            if strong_element and strong_element.find("dag") > 0 and len(strong_element) < 9:
                href_element = a_element.findChild("a")['href']
                if href_element:
                    list_days_urls.append(href_element)
    return list_days_urls

def get_recipes_ingredients(list_days_urls:list) -> tuple[list,list]:

    recipe_names_list = []
    list_quantity_ingredient = []
    
    for day_url in list_days_urls:
        day_page = get_page_as_soup(day_url)
        recipe_name = day_page.find("h1", class_="entry-title fn").string
        recipe_names_list.append([recipe_name, day_url])
        
        ingredients_list = day_page.find_all("li", class_="wprm-recipe-ingredient")
        
        for ingredient_item in ingredients_list:
            quantity = ""
            ingredient = ""
            if ingredient_item.findChild("span", class_="wprm-recipe-ingredient-amount"):
                quantity = ingredient_item.findChild("span", class_="wprm-recipe-ingredient-amount").string
            if ingredient_item.findChild("span", class_="wprm-recipe-ingredient-name"):
                ingredient = ingredient_item.findChild("span", class_="wprm-recipe-ingredient-name").string
            list_quantity_ingredient.append([quantity,ingredient])
            
    return recipe_names_list, list_quantity_ingredient

def scrape_recipe_names_ingredients(most_recent_week_url:str) -> tuple[list,list]:
    
    list_days_urls = get_days_urls(most_recent_week_url)
                    
    recipe_names_list, list_quantity_ingredients = get_recipes_ingredients(list_days_urls)
            
    return recipe_names_list, list_quantity_ingredients


def main():
    
    recipe_names_list, list_quantity_ingredients = scrape_recipe_names_ingredients()

if __name__ == "__main__":
    main()