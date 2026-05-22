# TODO - Add full product catalog (Food/Cosmetics/Spirituals/Nursery) with images

## Step 1: Verify current setup
- [x] Read existing frontend product rendering logic
- [x] Read backend `/products` endpoint logic
- [x] Inspect current DB schema + seeding script (`backend/setup_db.py`)

## Step 2: Implement catalog update
- [ ] Update `backend/setup_db.py` so it seeds/updates ALL products from the provided lists
- [ ] Ensure `image_url` is set to a placeholder (since images were not provided) for every product
- [ ] Fix/normalize names so duplicates/misspellings in lists are consistent

## Step 3: Seed safely
- [x] Modify seeding logic to be idempotent (avoid skipping when products exist)
- [x] Add a small update strategy: insert missing categories/products; optionally update image_url/price/benefits


## Step 4: Run & verify
- [ ] Run backend or `setup_db.py` to seed DB
- [ ] Verify `/api/products` returns full category tree and products
- [ ] Open `frontend/products.html` and confirm filtering works

## Step 5: Fix DB setup connectivity issues
- [x] Update `backend/setup_db.py` to add connection diagnostics (host/user/db/port) and a short retry
- [ ] Rerun `python backend/setup_db.py` and confirm DB seed completes


