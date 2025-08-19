import operator
from datetime import datetime

from app.data_io import load_json_data, write_json_data


class ProductItem:
    def __init__(self, product_id, title, release_date, price, image=None, rating=None, ):
        self.id = product_id
        self.title = title
        self.release_date = release_date
        self.image = image
        self.rating = float(rating)
        self.price = price

    def __str__(self):
        return f"{self.title}\t{self.release_date}\t{bool(self.image)}\t{self.rating}\t{self.price}"
    
    def update(self, new_data):
        # Empty field is not updated
        for k, v in new_data.items():
            if v:
                setattr(self, k, v)


class ProductDatabase:
    def __init__(self):
        self.product_item_list = list()
        self.product_dict_data = load_json_data()
        self.product_title_list = self.get_title_list()
    
    def item_to_data(self):
        json_data = list()
        for product in self.product_item_list:
            json_data.append(product.__dict__)
        return json_data

    def load_data(self):
        for product_dict in self.product_dict_data:
            product = ProductItem(product_id=product_dict["id"],
                          title=product_dict["title"],
                          release_date=product_dict["release_date"],
                          image=product_dict["image"],
                          rating=product_dict["rating"],
                          price=product_dict["price"])
            self.product_item_list.append(product)

    def get_item_by_title(self, title) -> ProductItem:
        for product_item in self.product_item_list:
            if product_item.title == title:
                return product_item

    def add_item_from_dict(self, product_dict):
        product_dict["id"] = len(self.product_item_list)
        new_item = ProductItem(product_id=product_dict["id"],
                             title=product_dict["title"],
                             release_date=product_dict["release_date"],
                             image=product_dict["image"],
                             rating=product_dict["rating"],
                             price=product_dict["price"])
        self.product_item_list.append(new_item)
        self.product_dict_data.append(product_dict)
        write_json_data(self.product_dict_data)
    
    def edit_item_from_dict(self, edit_title, product_dict: ProductItem):
        product_edit = self.get_item_by_title(edit_title)
        product_edit.update(product_dict)
        self.product_dict_data = self.item_to_data()
        write_json_data(self.product_dict_data)
    
    def delete_item(self, delete_title):
        product_delete = self.get_item_by_title(delete_title)
        self.product_item_list.remove(product_delete)
        self.product_dict_data = self.item_to_data()
        write_json_data(self.product_dict_data)
    
    def search_by_title(self, search_title) -> list[ProductItem]:
        matched_items = []
        for product_item in self.product_item_list:
            if search_title in product_item.title:
                matched_items.append(product_item)
        return matched_items

    def sort_item_by_rating(self, top=None):
        self.product_item_list = sorted(self.product_item_list, 
                                      key=operator.attrgetter('rating'),
                                      reverse=True
                                      )
        if top:
            return self.product_item_list[top]
    
    def sort_item_by_title(self, top=None):
        self.product_item_list = sorted(self.product_item_list, 
                                      key=operator.attrgetter('title')
                                      )
        if top:
            return self.product_item_list[top]
    
    def sort_item_by_date(self, top=None):
        self.product_item_list = sorted(self.product_item_list, 
                                      key=lambda x: format_date(x.release_date),
                                      reverse=True)
        if top:
            return self.product_item_list[top]
    
    def get_title_list(self):
        title = [product["title"] for product in self.product_dict_data]
        return title

def format_date(date_text):
    return datetime.strptime(date_text, '%b %Y')

def date_to_text(date:datetime):
    return date.strftime("%b %Y")