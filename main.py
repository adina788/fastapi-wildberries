from fastapi import FastAPI
from mysite.api import (user_profile, category, product, image_product, review, auth, cart,
                        cart_item, favorite, favorite_item, refresh_token)
from mysite.admin.setup import setup_admin


wildberries_app = FastAPI(title='Wildberries_AI25')
wildberries_app.include_router(user_profile.user_router)
wildberries_app.include_router(category.category_router)
wildberries_app.include_router(product.product_router)
wildberries_app.include_router(review.review_router)
wildberries_app.include_router(image_product.image_product_router)
wildberries_app.include_router(cart.cart_router)
wildberries_app.include_router(cart_item.cart_item_router)
wildberries_app.include_router(favorite.favorite_router)
wildberries_app.include_router(favorite_item.favorite_item_router)
wildberries_app.include_router(refresh_token.refresh_token_router)
wildberries_app.include_router(auth.auth_router)

setup_admin(wildberries_app)