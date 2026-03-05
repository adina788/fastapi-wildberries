from sqladmin import ModelView
from mysite.db.models import (UserProfile, Category, Product, ImageProduct, Review, Cart, CartItem,
                              Favorite, FavoriteItem, RefreshToken)



class UserProfileView(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]

class CategoryView(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

class ProductView(ModelView, model=Product):
    column_list = [Product.id, Product.product_name]

class ImageProductView(ModelView, model=ImageProduct):
    column_list = [ImageProduct.id, ImageProduct.image]

class ReviewView(ModelView, model=Review):
    column_list = [Review.id, Review.comment]

class CartView(ModelView, model=Cart):
    column_list = [Cart.id, Cart.user_id]

class CartItemView(ModelView, model=CartItem):
    column_list = [CartItem.id, CartItem.cart_id]

class FavoriteView(ModelView, model=Favorite):
    column_list = [Favorite.id, Favorite.user_id]

class FavoriteItemView(ModelView, model=FavoriteItem):
    column_list = [FavoriteItem.id, FavoriteItem.favorite_id]

class RefreshTokenView(ModelView, model=RefreshToken):
    column_list = [RefreshToken.id, RefreshToken.token]