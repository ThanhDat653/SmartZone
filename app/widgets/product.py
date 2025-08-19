import webbrowser
import os

from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QColorConstants
from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsDropShadowEffect

from config import Config
try:
    from app import Ui_ProductColumn
except ImportError:
    pass
from app.models import ProductItem


class ProductItemWidget(QWidget):
    STYLE_LOCATION = os.path.join(Config.UI_DIR, "style_product.qss")
    UI_LOCATION = os.path.join(Config.UI_DIR, "product_column.ui")
    def __init__(self, product:ProductItem):
        QWidget.__init__(self)
        try:
            self.ui = uic.loadUi(self.UI_LOCATION, self)
        except FileNotFoundError:
            self.ui = Ui_ProductColumn()
            self.ui.setupUi(self)

        with open(self.STYLE_LOCATION, "r") as style_file:
            style_config = style_file.read()
        self.setStyleSheet(style_config)

        self.product = product
        self.display_description()

        Animation.drop_shadow_on_hovered(self, self)
        
       

    def display_description(self):
        description_text = str(self.product.rating) +"/10"
        img_pixmap = QPixmap(self.product.image)
        self.ui.productTitle.setText(self.product.title)
        self.ui.productRating.setText(description_text)
        self.ui.productPrice.setText(str(self.product.price))
        self.ui.productView.setPixmap(img_pixmap)

    def open_link(self, url):
        if url != 'None':
            webbrowser.open(url)


class Animation:
    def drop_shadow_on(self, target_widget):
        effect = QGraphicsDropShadowEffect(target_widget)
        effect.setColor(QColorConstants.White)
        effect.setOffset(*Config.DROP_SHADOW_OFFSET)
        effect.setBlurRadius(Config.DROP_SHADOW_BLUR_RADIUS)
        target_widget.setGraphicsEffect(effect)

    def drop_shadow_off(self, target_widget):
        target_widget.setGraphicsEffect(None)

    def drop_shadow_on_hovered(self, target_widget:QLabel):
        target_widget.enterEvent = lambda x: Animation.drop_shadow_on(self, target_widget)
        target_widget.leaveEvent = lambda x: Animation.drop_shadow_off(self, target_widget)