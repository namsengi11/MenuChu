# MenuChu

## Plan
1. CLI program that takes in user input and returns results
   - Python for easy data management and analysis
3. Use vectors to describe characteristics of menus
   - Ingredient vector
   - Taste vector
   - Description vector
   - Difficulty (Cooking / Deliverable / Commonness) vector
   - All must be combined in one matrix as different columns.
   - Similar foods must have similar vectors
4. Elimination process
   - Recommend random food / take input from user and analyze its vector to provide similar food
   - If accepted, reset
   - If rejected, keep record of rejected food and recommend other foods in the database that has the furthest vector distance.
5. (Future) After recommendation algorithm/database is build, create tinder-like frontend
   - Swipe left/right until accepted
   
