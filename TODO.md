# TODO

- [ ] Fix Shop (products.html + products.js) so category-wise tabs show correct products AND images.
- [ ] Backend products endpoint should return per-subcategory product images already category-wise (done check).
- [ ] Ensure frontend uses product.image_url directly (no wrong global replace).
- [ ] If some category images are coming wrong, update backend mapping using backend/product_images.py (replace image_url assignment).
- [x] Backend images come from DB product.image_url and store_link mapping.
- [x] Fix wrong image assignment in DB generation (setup_db / image resolver) using backend/product_images.py (category/subcategory wise).

- [ ] Run server and verify: Food shows food images, Natural Cosmetics shows cosmetics images, etc.


